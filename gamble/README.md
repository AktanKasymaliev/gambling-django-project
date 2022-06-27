# Pseudo slot spinner game

How to start?
** 1. Start project with docker or CMD:
* 2. Create superuser 
* 3. Login into admin panel, then select `Slot Machines`.
        ![Screenshot](/readme_images/slotmachine.png?raw=true "Admin")

* 4. Create one machine.
* 6. Go to ```http://localhost:8000/api/spin/auto-complete/<slot machine id>/```
        P.S Here you can automatically fill all slots (for comfort)
        ![Screenshot](/readme_images/auto-complete.png?raw=true "Auto complete slots")

* 7. Now you can open postman or something else, and send POST request to:
        `http://<HOST>/api/spin/<slot machine id>/`
        ![Screenshot](/readme_images/spin.png?raw=true "Spin")

* Note: 1. While the game is going, you can see info about users, just send GET request on the same URL
        2. `http://<HOST>/swagger/` - Here you can see APIes
