export let templates = [
    `
          <form enctype="multipart/form-data" action="" method="post" id="create-post-form">
                 {% csrf_token %}
                 <input placeholder="عنوان پست ..." name="title" id="post-title" type="text" maxlength="200">
                 <textarea placeholder="متن پست ..." name="body" id="post-body" max-length = "100000"></textarea>
                 <input placeholder="تاریخ انتشار  (اختیاری جهت انتشار پست در آینده)" name="date" class="datepick" type="text">
                 <input name="" type="file">
                 <button>ایجاد پست</button>
          </form>
    ` , 

]