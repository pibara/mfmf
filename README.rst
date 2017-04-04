Mediocre Forensic Module Framework (MFMF)
=========================================

This repository contains the Mediocre Forensic Module Framework (MFMF). This minimal framework is meant as an example and fork-point for developers wanting to create a forensic module framework on top of the MattockFS computer forensics framework.

MattockFS is a computer-forensics data-archive and local message-bus component implemented as user-space file-system that is designed to enable the creation of a schalable and robust computer forensic framework. MattockFS though is not a forensic framework on its own. A full-fledged computer forensic framework will require at least three aditional main components:

* A Forensic Module Framework
* A modules collection.
* A networking and load-balancing mesh-up 

Given that MattockFS is a spare-time project that by itself already eats up quite some time for me as it's author,
I'm not going to be able to both spread my time over the three main components of an envisioned digital forensic 
framework and guarantee sufficient quality. Understanding however that building these other components completely from
scratch could have a steep learning curve that might scare potential developers away, the code-base in this repository 
is meant for two purposes:

* As a sceleton implementation of a basic Forensic Module Framework.
* As an envinronment for testing modules without a real Forensic Module Framework.

Anyone open to trying to build a full-fledged computer forensic module framework, please consider forking this project
and renaming it to Forensic Module Framework (fmfw). The example modules should try to use fmfw first if available and 
will only revert to using mfmf if fmfw is not available. 

This implementation is basically a a showcase of how MattockFS could work with a simple setup that glues together the following mean forensic mofule framework components:

* A core event-loop that polls nd works with multiple mattockFS mount points.
* A meta-data based router for routing jobs through their tool-chain.
* Serialization logic.
* Throttling logic.
* Evidence tree-walking logic.

The Mediocre Forensic Module Framework (MFMF) includes what are basically the most trivial and/or naive versions of each of these components. A basic event-loop, a mime-type only stateless router, a json serializer, a do-nothing throttler and a basic tree walker. Fixing the router and the trottler should be top priority for any Forensic Module Framework (fmfw) implementation based on MFMF.

While this repo is meant mostly as help to get other projects a leg-up and feature implementation will remain low priority at least untill there are zero issues left in MattockFS, pull-requests are very much welcomed, as are issues if these pertain to bugs or major oversights. If you want me to link to your MattockFS based project from this readme, also just submit an issue.
