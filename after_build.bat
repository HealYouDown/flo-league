rmdir "./app/static" /S /Q
move build "./app/"
rename "./app/build" "static"
move "./app/static/static/js" "./app/static" 
rmdir "./app/static/static" /S /Q
