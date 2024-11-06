import hrequests

url = "https://www.indeed.com/m/viewjob?jk=3174438e156ea133&from=serp"

headers = {
  'Host': 'www.indeed.com',
  'Upgrade-Insecure-Requests': '1',
  'User-Agent': 'Mozilla/5.0 (Linux; Android 11; Phone Build/RQ1A.210105.003; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/83.0.4103.120 Mobile Safari/537.36 Indeed App 186.0',
  'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
  'X-Requested-With': 'com.indeed.android.jobsearch',
  'Sec-Fetch-Site': 'same-origin',
  'Sec-Fetch-Mode': 'navigate',
  'Sec-Fetch-User': '?1',
  'Sec-Fetch-Dest': 'document',
  'Accept-Encoding': 'gzip, deflate, br',
  'Accept-Language': 'en-US,en;q=0.9',
  'Content-Length': '2',
  'Content-Type': 'text/plain',
  'Cookie': 'app="186.0,Android"; CTK=1ibuc0ni3jdln804; SHARED_INDEED_CSRF_TOKEN=7P6GnRbNoPeLUYZIbOz3ZQMbBwvyR3ZQ; __cf_bm=qcYxlpHI_SA0X5NEmk4vllZswHGyhAdCNbvGnY1L.Do-1730889731-1.0.1.1-T9SUJzUWA9tCg7_5Lwx5ZZ6DgwkvGzsH5crxIbv.Kc49AReup8bFHobk31Q80qIW9MsFB4opgoAl9noKvNm2EQ; _cfuvid=KPA23y24v3UyZHC9b9lFx_C6yC2skSPGXYvu2kZ00bY-1730889731705-0.0.1.1-604800000; INDEED_CSRF_TOKEN=1Xt4EuUKe5n6OwQvTAtG2EKrRjaavBH6; LV="LA=1730817318:CV=1730817318:TS=1730817318"; RQ="q=government+tactical+solutions+llc&l=&ts=1730817318491"; indeed_rcc="app:LV:CTK"'
}

response = hrequests.request("GET", url, headers=headers)

print(response.status_code)
