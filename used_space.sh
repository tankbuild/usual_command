for i in ./* ; do
	if [ -d "$i" ]; then
		cd $i
		echo $i :  $(du -sh)
		cd ..
	fi
done
