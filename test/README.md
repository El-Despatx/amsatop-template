# About this folder

This folder contains multiple testing environments for the procfs (process file system).

## Folder structure 

```text
.
├── prac_2_1 (tests for the PRAC 2.1)
│   └── one
│   │   └── ... => (processes/threads/kthreads folders)
│   │   └── htop.png => Image of the hierarchy on htop
│   │   └── proc.json => Relationship of what that pid/tid is.
│   └── two
│   │   └── ... => same structure as one...
│   └── test_xxx_xxx.py => where the tests live
├── prac_2_2 (tests for the PRAC 2.2)
│   └── ... (same structure as PRAC 2.2)
├── prac_2_2 (tests for the PRAC 2.3)
│   └── ... (same structure as PRAC 2.3)
├── conftest.py => helper functions for the tests that you probably don't want to read.
├── README.md
```

## Description
- The `one`, `two`, etc. directories each contain a simulated proc filesystem environment.

- Each simulated proc filesystem environment contains: 
  - A `htop.png` image, which shows how htop shows the processes of the current test.
  - A `proc.json` file, which tells you the relationship between the identifier and if it's a process, thread, etc.
- The `utils` folder contains code and helper scripts used by the teachers to create the examples. You’re free to ignore these or use them as needed.
