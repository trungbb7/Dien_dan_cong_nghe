from django.shortcuts import redirect, render

from comment.forms import QuestionForm
# Create your views here.


def index(request):
    print("da vao day")
    return render(request, "comment/index.html")


def askquestion(request):
    return render(request, "comment/askquestion.html")



def ask_question(request):
    if request.method == 'POST':
        form = QuestionForm(request.POST)
        if form.is_valid():
            # Xử lý dữ liệu hợp lệ
            question_title = form.cleaned_data['question_title']
            question_description = form.cleaned_data['question_description']
            related_tags = form.cleaned_data['related_tags']
            

            return redirect('comment/index.html')
    else:
        form = QuestionForm()
    
    return render(request, 'comment/askquestion.html', {'form': form})