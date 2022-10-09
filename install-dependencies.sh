#!/bin/bash

is_installed_python_requirements=false
is_installed_libjpeg8_dev=false

if [ "$(whoami)" != "root" ] ; then
    echo -e "You must run this script as root."
    exit
fi

sudo apt-get update
# sudo apt-get upgrade -y

function if_continue(){
    while :; do
        echo  -e "(yes/no) \c"
        read input_item
        if [ $input_item = "yes" ]; then
            break
        elif [ $input_item = "no" ]; then
            return 0
        else
            echo -e "Input error, please try again."
        fi
    done
    return 1
}

function end(){
    print_result
    echo -e "Exiting..."
    exit
}

function print_result(){
    echo -e "Installation result:"
    echo -e "python requirements  \c"
    if $is_installed_python_requirements; then
        echo -e "Success"
    else
        echo -e "Failed"
    fi
    echo -e "libjpeg8-dev  \c"
    if $is_installed_libjpeg8_dev; then
        echo -e "Success"
    else
        echo -e "Failed"
    fi
}

###################################
# Install python requirements #
###################################

echo -e "\nInstalling python requirements \n"
if pip3 install -r requirements.txt; then
    echo -e "    Successfully installed python requirements \n"
    is_installed_python_requirements=true
else
    echo -e "    Failed to installed python requirements \n"
    echo -e "    Do you want to skip this? \c"
    if_continue
    if [ $? = 1 ] ; then
        echo -e "    Skipped python requirements installation."
    else
        end
    fi
fi

###################################
# Install libjpeg8-dev #
###################################

echo -e "\nInstalling libjpeg8-dev \n"
if sudo apt-get install libjpeg8-dev -y; then
    echo -e "    Successfully installed libjpeg8-dev \n"
    is_installed_libjpeg8_dev=true
else
    echo -e "    Failed to installed libjpeg8-dev \n"
    echo -e "    Do you want to skip this? \c"
    if_continue
    if [ $? = 1 ] ; then
        echo -e "    Skipped libjpeg8-dev installation."
    else
        end
    fi
fi

###################################
# Export Paths #
###################################

# echo -e "Export paths. \n"
# echo -e export LD_LIBRARY_PATH=/usr/local/lib/ >> ~/.bashrc
# echo -e export LD_LIBRARY_PATH=/usr/local/lib/ >> ~/.profile
# source ~/.bashrc
# echo -e "complete. \n"

###################################
# Enable I2C1 #
###################################

# Add lines to /boot/config.txt
echo -e "Enalbe I2C \n"
egrep -v "^#|^$" /boot/config.txt > config.txt.temp  # pick up all uncomment configrations
if grep -q 'dtparam=i2c_arm=on' config.txt.temp; then  # whether i2c_arm in uncomment configrations or not
    echo -e '    Seem i2c_arm parameter already set, skip this step \n'
else
    echo -e '    dtparam=i2c_arm=on \n' >> /boot/config.txt
fi
rm config.txt.temp
echo -e "complete\n"

print_result

echo -e "The stuff you have change may need reboot to take effect."
echo -e "Do you want to reboot immediately? \c"
if_continue
if [ $? = 1 ]; then
    echo -e "Rebooting..."
    sudo reboot
else
    echo -e "Exiting..."
    exit
fi
