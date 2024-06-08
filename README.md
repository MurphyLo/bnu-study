# bnu-study
***library reverie***

### requirements

- `pyexecjs`
- `requests`
- `bs4`
- `des.js`

### how to

1. Install required packages.
2. Modify `main.py`
    - fill in `u` and `p`.
    - change `start`, `end` to your desired time range for reverie.  
    - change `seat_id` to your favorite seat id (id parameter from uri `/freeBook/ajaxGetTime` in Developer Tools's Network page).
      <br><img src="https://github.com/MurphyLo/bnu-study/assets/69335326/37d67ad4-2531-41f9-a5ea-f956c93c7d9b" alt="" width="500">
3. Make sure `main.py`, `des.js` are in the same directory and run `main.py` **before 19:30**.

### automate with crontab

1. Include shebang line at the beginning of `main.py`: `#!/path/to/python_interpreter`
2. `chmod u+x /path/to/main.py`.
3. `crontab -e`
4. Add `29    19    *    *    *    /path/to/main.py >> /path/to/seat.log 2>&1`
