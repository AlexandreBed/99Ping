# 99Ping
Projet_99Ping

Bonjour!

---------------------Les paths de ou place chaqun des fichiers---------------------


-----------------------------------------------------------------------------------
pcf _keyboard.py peux etre placer dans un directory sur le desktop
EX /home/pi/Desktop/99Ping/pcf_keyboard.py
-----------------------------------------------------------------------------------
Meme chose pour le startup.sh
EX /home/pi/Desktop/99Ping/startup.sh
-----------------------------------------------------------------------------------
Pour les fichier de type .log sont au niveau de l'utilisateur
EX /home/pi/pcfkeyboard.log
EX /home/pi/startup.log
-----------------------------------------------------------------------------------
Les ficher de type .service sont dans le fichier system du systemd
EX /etc/systemd/system/startup.service
EX /etc/systemd/system/pcfkeyboard.service
-----------------------------------------------------------------------------------
Pour le fichier workingpcfconfig.txt il vas falloire copier le contenue dans le fichier config.txt du CM5 pour le faire fonctionner.
EX /boot/firmware/config.txt

Pour faire cela faire la commande :
sudo cp workingpcfconfig.txt /boot/firmware/config.txt
-----------------------------------------------------------------------------------
Le fichier SSM2518.dts est un overlay fait par Analogue Devices qui vas etre placer
avec les autres overlays du system.
EX /boot/firmware/overlays/ssm2518-overlay.dts

Une foit mis la il vas falloir le compiler en .dtbo

-----------------------------------------------------------------------------------
Pour avoir une experience complete du projet il faut installer Retro pie sur le CM5

Pour avoir des jeux aller sur https://www.romsgames.net/
pour jouer au jeux il faut les placer dans le fichier de sa propre console
EX /home/pi/RetroPie/roms/gba/Pokemon_ FireRed Version.zip





