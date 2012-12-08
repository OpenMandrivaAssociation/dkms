#!/bin/awk -f
# Loads the modules called with if necessary
# Based upon original script from Anssi Hannula:
#  <http://archives.mandrivalinux.org/cooker/2009-03/msg00835.php>

# TODO: investigate if this could be replaced with simple calls to
# udevadm trigger --attr-match=modalias=foo

BEGIN{
  FS="="

  # no arguments, sucessfully do nothing
  if (ARGC < 2) {
    exit(0)
  }

  for (i=1; i<ARGC; ++i)
    modlist=modlist" "ARGV[i]

  # get the aliases of the specified modules converted to regexps
  while ("modinfo -F alias "modlist | getline)
  {
    gsub("\\*", ".*")
    gsub("\\?", ".")
    sub(".*", "^&$")
    modaliases[$0]=$0
  }

  while ("udevadm info --export-db" | getline) {
    if (! /^E: (PCI_CLASS|DRIVER|MODALIAS)/) { continue }
    # do not modprobe devices that already have a driver
    if (/^E: DRIVER=./) { skip=1; continue }
    if (/^E: PCI_CLASS=3....$/) { disp=1; continue }
    if (/^E: MODALIAS=/ && skip) { skip=0; disp=0; continue }

    # modprobe existing device aliases ($2) provided by the given modules
    if (/^E: MODALIAS=/) {
      for (modalias in modaliases)
        if ($2 ~ modalias)
          if (disp) {
            system("display_driver_helper --load-dkms-autoload \""ARGV[1]"\" \""$2"\"")
          } else {
            system("modprobe --use-blacklist \""$2"\"")
          }
      disp=0
    }
  }
}
