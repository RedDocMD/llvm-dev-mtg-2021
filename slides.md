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
Examples of bugs may include null-pointer de-reference, un-closed files, leaked memory, etc. -->