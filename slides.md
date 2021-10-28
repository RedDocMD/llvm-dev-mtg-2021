---
theme: default
title: 'LLVM Dev Mtg 2021'
titleTemplate: '%s'
class: 'text-center'
highlighter: shiki
monaco: true
colorSchema: 'dark'
---

<div class="text-5xl text-light-300 pt-5">Clang Static Analyzer:<br/>A Tryst with Smart Pointers</div>
<div class="text-3xl pt-15 text-amber-300">Deep Majumder</div>
<div class="text-2xl pt-2 text-amber-300">Indian Institute of Technology, Kharagpur</div>
<div class="flex justify-center h-35 pt-10"><img src="/imgs/wyvern.png" /></div>
<div class="pt-4 text-blue-300">LLVM Developers' Meeting</div>
<div class="pt-1 text-blue-300">November 17, 2021</div>

---
---

<h1 class="text-amber-300">GSoC 2021</h1>
<div></div>

The talk revolves around my Google Summer of Code project this year under The LLVM Foundation. The project was <span class="font-bold text-light-blue-300">Making Smart Pointer Checkers default checkers in the Static Analyzer</span>.

<v-click>

My mentors were:

- Artem Dergachev (Apple Inc.)
- Gábor Horváth (Microsoft Corp.)
- Valeriy Savchenko (Apple Inc.)
- Raphael Isemann (Vrije Universiteit Amsterdam)

</v-click>

---
---

<h1 class="text-amber-300">What is the Clang Static Analyzer?</h1>
<div></div>

The Clang Static Analyzer (CSA) is a static-analysis framework that uses <span class="font-bold text-light-blue-300">symbolic execution</span> over all possible paths in a program to flag various buggy scenarios.

<div v-click class="flex justify-center pt-3 pb-2 h-85">
  <img src="/imgs/csa-intro.png">
</div>

<!-- Key point being the symbolic-execution, that is, the code is not actually run
Examples of bugs may include null-pointer de-reference, un-closed files, leaked memory, etc. 
Explain the diagram, mention that the cases are indicative -->

---
---

The CSA tries to have no (low) false positives. This means:

- A bug reported by the CSA is <span class="text-red-400">definitely</span> a bug.
- Absence of bug reports by the CSA does <span class="text-red-400">not</span> indicate absence of bugs.

This is different from the model followed by some other static analysis systems, such as the one in Rust.

---
---

<h1 class="text-amber-300">It's Checkers all the way down!</h1>
<div></div>

Checkers are the backbone of the CSA. 

<v-click>

Checkers can:

- Create data
- Modify existing data
- Use the data to detect bugs

</v-click>

<v-click>

Roughly speaking, <span class="text-blue-400">data</span> stands for <span class=text-red-300>constraints</span> on the possible values of a variable (or expression) at some point in the program. Also, we can store <span class="text-blue-400">metadata</span> to help dealing with complex scenarios.

</v-click>

---
---

For dealing with smart-pointers, we have currently have two checkers:

1) `SmartPtrModelling`, which actually creates the requisite data
2) `SmartPtrChecker`, which uses the data to detect null-dereferences

This de-coupling allows us to have <span class="text-teal-400">multiple</span> checkers to model the various smart-pointers, while having a *single checker emit the bug reports*.

---
layout: tee
---

<h1>How is it modelled?</h1>
<div />

`SmartPtrModelling` models the behaviour of `std::unique_ptr` by keeping track of the <span class="text-teal-400 italic">nullity of the raw-pointer inside the smart-pointer</span>.

::left::

```cpp{1-5,11|1,6-11|all}
void foo() {
    unique_ptr<int> ptr = make_unique<int>(13);
    // ptr definitely is not null now.
    cout << *ptr << "\n";
    // This statement is safe.
    ptr.reset();
    // ptr now is definitely null.
    magicFunc(*ptr);
    // This statement is definitely a 
    // null-ptr dereference.
}
```

::right::

```cpp{none|1-4,11|1,5-11|all}
void bar(unique_ptr<int> ptr) {
    // At this point we know nothing about ptr
    *ptr;
    // Since we aren't sure, we emit no report here
    if (!ptr) {
        // We are now sure that ptr is null here
        magicFunc(*ptr);
        // This statement is definitely a 
        // null-ptr dereference.
    }
}
```

---
---

<h1>What is there to model?</h1>
<div />

<div class="text-3xl text-emerald-400 font-extrabold">Everything!</div>

<v-click>

When we are modelling a C++ class like `std::unique_ptr`, we need to model all aspects of it. This includes modelling at least all <span class="text-blue-300">member</span> functions, <span class="text-blue-300">constructors</span>, and <span class="text-blue-300">destructors</span>.

</v-click>

<v-click>

The aim of modelling a class in a checker is to <span class="text-blue-300">add</span> information which is specific to the semantics of the class at hand.

</v-click>

<v-click>

This information is not necessarily discoverable automatically because the source code <span class="text-red-400">may not be available</span>. After all, the interface to a C++ library is via the header file, which may not contain all the code. 

</v-click>

---
---

<h1>The Perils of Incomplete Modelling</h1>
<div />

<span class="font-bold text-red-400">Loss of information:</span> Suppose we don't model the `reset()` method for `std::unique_ptr`, and assume it's source code is not available. 

CSA will default to <span class="text-blue-300">conservative evaluation</span>, which basically <span class="text-red-400">removes</span> information which may have been modified by the modelled method.

<v-click>

Then, the following code will report no errors, when there is obviously one (a *false-negative*).

```cpp
void foo() {
    unique_ptr<string> strPtr = make_unique<string>("Oh no!");
    strPtr.reset();
    auto len = strPtr->size(); // This is null-pointer dereference!
    // But we have no warning!
}
```

</v-click>

---
---

<span class="font-bold text-red-400">Inconsistent information:</span> Suppose we don't model the `destructor` of `std::unique_ptr`. 

Since the code for the destructor is usually available, CSA will automatically evaluate it, in a process known as <span class="text-blue-300">inlining</span>.

<v-click>

The destructor for `std::unique_ptr` is (very) roughly as follows:

```cpp
~unique_ptr() {
    if (rawPtr)
        get_deleter()(rawPtr);
        // This defaults to `delete rawPtr;`
}
```

</v-click>

<v-click>

Sometimes "bug" reports generated by the CSA are <span class="text-red-400">suppressed</span> when we believe that they are probably false-positives. "Bugs" that come from the standard library are one such class.

</v-click>

---
---

But as a side-effect, the following code's leak warning (which comes a different checker, `MallocChecker`) also gets suppressed.


```cpp
void bad() {
    auto smart = std::unique_ptr<int>(new int(13));
    auto raw = new int(29);
    // There is a leak here.
    // But that warning gets suppressed!
}
```

<v-click>

<span class="text-blue-300">Moral of the story: </span> Model C++ classes completely to avoid such side-effects.

</v-click>

---
---

<h1>Closure</h1>
<div />

<v-clicks>

- We have a almost complete model for `std::unique_ptr` in `SmartPtrModelling`
- The current modelling provides a framework for modelling other smart-pointers, such as `std::shared_ptr` or `std::weak_ptr`.
- New developers are very much welcome! Please feel free to hit us up on the cfe-dev mailing list.

</v-clicks>