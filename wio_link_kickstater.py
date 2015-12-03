#!/usr/bin/env python
# copyright 2015 seeed, wangtengoo7@gmail.com
import requests
import random
import time

# Kickstarter_url = "https://www.kickstarter.com/projects/search.json?search=&term=%22Kris%20Cheng%22" #other ks project
# Kickstarter_url = "https://www.kickstarter.com/projects/search.json?search=&term=%22Pizza%20Book%22" #other ks project
Kickstarter_url = "https://www.kickstarter.com/projects/search.json?search=&term=%22Wio%20Link%22" #wio link ks
wio_link_led_url = "https://cn.iot.seeed.cc/v1/node/GroveLedWs2812/segment/0/"
wio_link_key = "access_token=ce9356cb1840fad3e09c9fd2c7b9865b"
wio_link_recorder = "https://cn.iot.seeed.cc/v1/node/GroveRecorder/play_once?access_token=ce9356cb1840fad3e09c9fd2c7b9865b"
wio_link_servo = "https://cn.iot.seeed.cc/v1/node/GroveServo/angle/"
USD_PLEDGED = 0
BACKERS_COUNT = 0

ONE_LED_USD = 2000

def get_rainbow(number):
    if number > 40:  #wiolink only support 40 led
        number = 40
    # color_items = ["FF0000", "FFA500", "FFFF00", "00FF00", "00FFFF", "0000FF", "9B30FF"]
    color_items = ["2F0000", "00002F", "2F2F00", "002F2F", "00FF00",]
    # color_items = ["2F0000","2F0000","2F0000","2F0000","2F0000","2F0000","2F0000"]
    # color_items = ["002F00","002F00","002F00","002F00","002F00","002F00","002F00"]
    # random.shuffle(color_items)
    if number <= len(color_items):
        color_items = color_items[0:number]
        color_items += ["000000"]*(40-number)
    else:
        color_items *= int(number/len(color_items))
        color_items.extend(color_items[:number%len(color_items)])
        color_items += ["000000"]*(40-number)
    rgb_hex_string = "".join(color_items)
    return rgb_hex_string

def update_display(usd):
    usd = int(usd)
    number = usd/ONE_LED_USD
    # print number
    rgb_hex_string = get_rainbow(number)
    # print rgb_hex_string
    url = wio_link_led_url + rgb_hex_string + "?" + wio_link_key
    requests.post(url)

def prompt_everbody(count):
    servo_degree_start = wio_link_servo + "10"
    servo_degree_end = wio_link_servo + "180"
    for i in range(count):
        # requests.post(servo_degree_start + "?" + wio_link_key)
        # time.sleep(1)
        # requests.post(servo_degree_end + "?" + wio_link_key)
        # time.sleep(1)
        requests.post(wio_link_recorder)
        time.sleep(2)


def ks_data_process(usd_pledged, backers_count):
    global USD_PLEDGED
    global BACKERS_COUNT
    usd_pledged = float(usd_pledged)
    backers_count = int(backers_count)

    if usd_pledged != USD_PLEDGED:
        print "usd_pledged plus:  " + str(usd_pledged - USD_PLEDGED)
        print "usd_pledged:       " + str(usd_pledged)
        update_display(usd_pledged)
        USD_PLEDGED = usd_pledged

    if backers_count > BACKERS_COUNT:
        print "backers_count:     " + str(backers_count)
        print time.asctime(time.localtime(time.time())) + "\n"
        prompt_count = backers_count - BACKERS_COUNT
        if BACKERS_COUNT > 0:
            prompt_everbody(prompt_count)
        BACKERS_COUNT = backers_count

def get_kickstarter():
    r = requests.get(Kickstarter_url)
    # print r.status_code
    # print r.json()
    data_json = r.json()

    if data_json is None:
        print "Status Code:" + r.status_code

    project = data_json.get('projects')[0]
    backers_count = project.get("backers_count")
    usd_pledged = project.get("usd_pledged")

    # print "usd_pledged:  " + str(usd_pledged )
    # print "backers_count:" + str(backers_count)

    ks_data_process(usd_pledged, backers_count)

def main():
    while True:
        get_kickstarter()
        time.sleep(5) #5s
    # update_display(40000)
    # prompt_everbody(5)

if __name__ == "__main__":
    main()
