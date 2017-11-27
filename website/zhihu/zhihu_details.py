from urllib import request
from pprint import pprint
import json
from pymongo import MongoClient

header = {
    'Cookie':'q_c1=aeb58fa09c9e475eb1038171398a576f|1496971539000|1496971539000; r_cap_id="MWQzZjAzZWRhMTcyNDk2OGExNWEzYWI4YTFhYTBiZTM=|1497243490|1ba580ac324ffea6dd8e5ce94b6c395ea2927886"; cap_id="MGFkYmY0MmYwZDY0NDlhNDk5ZTM1MDg3Y2E3MmYxMDg=|1497243490|9c6595a99dc1224d29810fd1100a3001d1dd955c"; d_c0="ADCCdVK-5guPTvmvzBI7v_GoR9qeBitK6IY=|1497243491"; _zap=54f1f19c-e7d4-4d84-9f79-a8d1d0346f5a; _ga=GA1.2.576220217.1497243504; _xsrf=487101397db6ee56abaade9e96be5873; s-q=mysql; s-i=17; sid=458e7o4o; __utma=51854390.576220217.1497243504.1497404428.1497421636.5; __utmc=51854390; __utmz=51854390.1497421636.5.5.utmcsr=hao123.com|utmccn=(referral)|utmcmd=referral|utmcct=/link/https/; __utmv=51854390.100-1|2=registration_date=20121030=1^3=entry_date=20121030=1; z_c0=Mi4wQUFEQTk5TVpBQUFBTUlKMVVyN21DeGNBQUFCaEFsVk5kS3hsV1FDVjNfZENJSnh2bkZHeEZZSXlOcnZpNzFraGJR|1497430050|abe1ebbbf3af2ec993301ada06a148c90a74e9fa'
}
offset = 20
url = 'https://www.zhihu.com/api/v4/questions/23289709/answers?sort_by=default&include=data%5B%2A%5D.is_normal%2Cis_collapsed%2Ccollapse_reason%2Cis_sticky%2Ccollapsed_by%2Csuggest_edit%2Ccomment_count%2Ccan_comment%2Ccontent%2Ceditable_content%2Cvoteup_count%2Creshipment_settings%2Ccomment_permission%2Cmark_infos%2Ccreated_time%2Cupdated_time%2Crelationship.is_authorized%2Cis_author%2Cvoting%2Cis_thanked%2Cis_nothelp%2Cupvoted_followees%3Bdata%5B%2A%5D.author.follower_count%2Cbadge%5B%3F%28type%3Dbest_answerer%29%5D.topics&limit=20&offset={}'.format(offset)
request_data = request.Request(url,headers=header)
data = request.urlopen(request_data).read()
data = json.loads(data.decode('utf-8'))

for item in data['data']:
    pprint(item['content'])