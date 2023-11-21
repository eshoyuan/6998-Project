document.getElementById('image-input').addEventListener('change', function(event) {
    var file = event.target.files[0]; // 获取用户选择的文件
    var reader = new FileReader(); // 创建 FileReader 对象

    reader.onload = function(e) {
        var preview = document.getElementById('preview-image'); // 获取显示图片的元素
        preview.src = e.target.result; // 设置图片源为读取到的数据
        document.getElementById('image-display').style.display = 'flex'; // 使用flex显示图片容器
    };

    reader.readAsDataURL(file); // 读取文件内容
});
document.getElementById('upload-button').addEventListener('click', function(event) {
    event.preventDefault(); // 阻止表单默认提交行为
    var fileInput = document.getElementById('image-input');
    
    console.log("Start uploading...");
    if(fileInput.files.length > 0) {
        var file = fileInput.files[0];
        var reader = new FileReader();

        reader.onloadend = function() {
            // 当读取操作完成后执行此函数
            var base64data = reader.result; // 图片的Base64编码

            // 调用AWS API Gateway客户端上传图片
            var params = {};
            var body = {body: base64data};
            console.log(base64data);
            var additionalParams = {
                headers: {
                    'Access-Control-Allow-Origin': '*',
                    'Access-Control-Allow-Headers': '*',
                    'Access-Control-Allow-Methods': '*',                }
            };

            sdk.uploadImagePost(params, body, additionalParams).then(function(response) {
                console.log('Image uploaded successfully:', response);
                // 处理成功响应
            }).catch(function(error) {
                console.error('Image upload failed:', error);
                // 处理错误响应
            });
        };

        reader.readAsDataURL(file); // 以DataURL的形式读取文件
    } else {
        alert('Please select a file to upload.');
    }
});
