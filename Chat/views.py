import json

from django.http import StreamingHttpResponse
from django.shortcuts import render, redirect

from Users.models import SiteUser
from Users.views import get_user_link, get_post_list, get_file_list, get_user_sidebar_widget
from .chat import chatCore
from .models import Chat


# chat.py 由于包含API的敏感信息故暂不提供

def chat(request):
    # 不允许访客查看聊天页面
    if (user_id:=request.session.get("login_user_id")) is None:
        return redirect("/user/login/")
    _user = SiteUser.objects.get(id=user_id)

    if request.method == "POST":
        # 如果存在用户输入，则保存用户输入再调用聊天模型
        _data = json.loads(request.body.decode())
        if user_input:=_data["user_input"]:
            _chat = Chat.objects.get(user=_user)
            json_data: [dict] = json.loads(_chat.messages)
            json_data.append({"role": "user", "content": user_input})
            _chat.messages = json.dumps(json_data, ensure_ascii=False)
            _chat.save()
        # 模拟输入数据
        stream = chatCore.chat(_user)
        return StreamingHttpResponse(stream, content_type="text/event-stream")
    else:
        context = {
            "messages": [],
            "sidebars": [
                get_user_sidebar_widget(request, _user),
                get_post_list(request, _user),
                get_file_list(request, _user),
            ]
        }
        try:
            _chat = Chat.objects.get(user=SiteUser.objects.get(id=user_id))
            for message in json.loads(_chat.messages)[1:]:
                message: dict[str, str]
                message["content"] = message["content"].replace("\n", "<br>")
                context["messages"].append(message)
        except Chat.DoesNotExist:
            pass
        return render(request, "Chat/chat.html", context)
