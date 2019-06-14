echo "INSTALL DOCBAO CRAWLER ON UBUNTU"
export install_dir="/home/$USER/docbao_crawler"
sleep 1
echo "Step 0: ensure python3, pip3 and curl are installed"
sleep 1
sudo apt update
sudo apt install python3
sudo apt install python3-pip
sudo apt install curl
sleep 1
echo "Step 1: install python libraries"
sleep 1
pip3 install -r requirements.txt
sleep 1
echo "Step 2: install firefox and xvfb"
sleep 1
sudo apt install firefox
sudo apt install xvfb
sleep 1
echo "Step 3: copy resources files"
sleep 1
sudo cp $install_dir/resources/firefox_driver/ubuntu/geckodriver /usr/bin
sleep 1
echo "Finish !"
