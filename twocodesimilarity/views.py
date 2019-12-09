from django.shortcuts import render
from .forms import CodeForm

from question.views import get_fingerprints_k_grams, get_suspicious_lines, get_k_grams, right_min, winnowing, tokenize_code, clean

def check_two_codes_similarity(request):
	context = {}
	form = CodeForm(request.POST or None)
	if form.is_valid():
		code1 = form.cleaned_data['code1']
		code2 = form.cleaned_data['code2']
		fp1, k_grams1 = get_fingerprints_k_grams(code1)
		fp2, k_grams2 = get_fingerprints_k_grams(code2)
		suspicious_part_code1, matched_fp = get_suspicious_lines(code1, fp1, fp2, k_grams1)
		suspicious_part_code2, matched_fp = get_suspicious_lines(code2, fp2, fp1, k_grams2)
		suspicious_part_code1 = suspicious_part_code1.replace("\t", "----")
		suspicious_part_code2 = suspicious_part_code2.replace("\t", "----")
		context['suspicious_part_code1'] = suspicious_part_code1.split("\n")
		context['suspicious_part_code2'] = suspicious_part_code2.split("\n")
		context['code1_similarity_percentage'] = (matched_fp/len(fp1)) * 100
		context['code2_similarity_percentage'] = (matched_fp/len(fp2)) * 100
	context['form'] = form
	return render(request, "twocodesimilarity/checktwocodes.html",context)
