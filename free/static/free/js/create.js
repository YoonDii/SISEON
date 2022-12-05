
//if 이미지 선택한 적 X -> 함수 실행 else 초기화 후 함수 실행
function setThumbnail(event) {
    if (setThumbnail === false) {
        for (var image of event.target.files) {
            var reader = new FileReader();

            reader.onload = function (event) {
                var img = document.createElement("img");
                img.setAttribute("src", event.target.result);
                document.querySelector("div#image_container").appendChild(img);
            };

            console.log(image);
            reader.readAsDataURL(image);
        }
    } else {
        //여기에 초기화 시키는 걸 적으면 안 되려나...

        for (var image of event.target.files) {
            var reader = new FileReader();

            reader.onload = function (event) {
                var img = document.createElement("img");
                img.setAttribute("src", event.target.result);
                document.querySelector("div#image_container").appendChild(img);
            };

            console.log(image);
            reader.readAsDataURL(image);
        }
    }
}
