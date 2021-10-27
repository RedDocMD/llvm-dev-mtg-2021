---
theme: default
class: 'text-center'
highlighter: shiki
monaco: true
---

<div class="text-5xl text-light-300">Clang Static Analyzer:<br/>A Tryst with Smart Pointers</div>
<div class="text-3xl pt-20 text-amber-300">Deep Majumder</div>
<div class="text-xl pt-2 text-amber-300">Indian Institute of Technology, Kharagpur</div>

---
class: 'text-2xl'
---

<h1 class="text-amber-300">GSoC 2021</h1>
<div></div>

The talk revolves around my Google Summer of Code project this year under The LLVM Foundation. The project was <span class="font-bold text-light-blue-300">Making Smart Pointer Checkers default checkers in the Static Analyzer</span>.

My mentors were:

- Artem Dergachev (Apple Inc.)
- Gábor Horváth (Microsoft Corp.)
- Valeriy Savchenko
- Raphael Isemann

---
class: 'text-2xl'
---

<h1 class="text-amber-300">What is the Clang Static Analyzer?</h1>
<div></div>

The Clang Static Analyzer (CSA) is a static-analysis framework that uses <span class="font-bold text-light-blue-300">symbolic execution</span> over all possible paths in a program to flag various buggy scenarios.

<div class="flex justify-center pt-3 h-85">
  <img src="/imgs/csa-intro.png">
</div>

<!-- Key point being the symbolic-execution, that is, the code is not actually run
Examples of bugs may include null-pointer de-reference, un-closed files, leaked memory, etc. 
Explain the diagram, mention that the cases are indicative -->

---
class: 'text-2xl'
---

The CSA tries to have no (low) false positives. This means:

- A bug reported by the CSA is <span class="text-red-400">definitely</span> a bug.
- Absence of bug reports by the CSA does <span class="text-red-400">not</span> indicate absence of bugs.

This is different from the model followed by some other static analysis systems, such as the one in Rust.

---
class: 'text-2xl'
---

<h1 class="text-amber-300">It's Checkers all the way down!</h1>
<div></div>

Checkers are the backbone of the CSA. Checkers can:

- Create data
- Modify existing data
- Use the data to detect bugs

Roughly speaking, <span class="text-blue-400">data</span> stands for <span class=text-red-300>constraints</span> on the possible values of a variable (or expression) at some point in the program. Also, we can store <span class="text-blue-400">metadata</span> to help dealing with complex scenarios.

---
class: 'text-2xl'
---

For dealing with smart-pointers, we have currently have two checkers:

1) `SmartPtrModelling`, which actually creates the requisite data
2) `SmartPtrChecker`, which uses the data to detect null-dereferences

This de-coupling allows us to have <span class="text-teal-400">multiple</span> checkers to model the various smart-pointers, while having a *single checker emit the bug reports*.