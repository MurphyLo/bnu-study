# bnu-study
***A Library Reverie***

### Prerequisites

- `pyexecjs` whispers to the wind
- `requests` as letters to the void
- `bs4` dreams of structure
- `des.js` holds secrets untold

### How to Begin

1. Gather the whispers, letters, dreams, and secrets.
2. In the heart of `main.py`, inscribe:
    - Your account number and password within `u` and `p`.
    - Time’s tender embrace between `start` and `end`.
    - Your chosen sanctuary, `seat_id`, where you'll dwell (find this in the labyrinth of Developer Tools’ Network page).
      <br><img src="https://github.com/MurphyLo/bnu-study/assets/69335326/37d67ad4-2531-41f9-a5ea-f956c93c7d9b" alt="" width="500">
4. Unite `main.py` and `des.js` beneath the same stars/directory, and let `main.py` dance **before 19:30**.

### Automate the Dance with Crontab

1. At dawn of `main.py`, mark it with a shebang: `#!/path/to/python_interpreter`.
2. Bless it with the power to execute: `chmod u+x /path/to/main.py`.
3. Call forth the crontab’s song: `crontab -e`.
4. Weave the following verse into the crontab’s fabric:
   `29    19    *    *    *    /path/to/main.py >> /path/to/seat.log 2>&1`
