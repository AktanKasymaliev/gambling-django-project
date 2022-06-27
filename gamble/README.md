# How to use?

How to start?
* I.   Start project with docker or CMD:
* II.  Create superuser 
* III. Login into admin panel, then select `Slot Machines`.
        ![Screenshot](/readme_images/slotmachine.png?raw=true "Admin")

* IV.  Create one machine.
* V.   Go to ```http://<HOST>/api/spin/auto-complete/<slot machine id>/```
          P.S Here you can automatically create all slots (for comfort)
          ![Screenshot](/readme_images/auto-complete.png?raw=true "Auto complete slots")

* VI.  Now you can open postman or something else, and send POST request to:
         `http://<HOST>/api/spin/<slot machine id>/`
         ![Screenshot](/readme_images/spin.png?raw=true "Spin")

* Note:  While the game is going, you can see info about users, just send GET request on the same URL
        ![Screenshot](/readme_images/info.png?raw=true "Spin")
        `http://<HOST>/swagger/` - Here you can see APIes