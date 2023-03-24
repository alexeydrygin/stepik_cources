import speedtest

test = speedtest.Speedtest()

down_speed = test.download()
up_speed = test.upload()

print('download ', down_speed)
print('upload ', up_speed)