from tools.util import format_str

s = '<strong>敏</strong><strong>感</strong>却不执着，坚定而又变通；稳重但又热烈，成'
res_search_dic = {}
data = res_search_dic["subject"] = format_str(s)
print(data)
print(len(data))
if len(data) > 50:
	res_search_dic["subject"] = data[:100] + '...'
	
print(res_search_dic)