    function simulateProgress() {
        var progressBar = document.getElementById("myProgressBar");
        var progressText = document.getElementById("progressText");

        var width = 1;
        var duration = 8000; // 8秒
        var interval = 10; // 更新间隔

        var increment = (interval / duration) * 100;

        var updateProgress = function () {
            if (width >= 100) {
                clearInterval(progressInterval);
            } else {
                width += increment;
                progressBar.style.width = width + "%";
                progressText.innerHTML = Math.round(width) + "%";
            }
        };

        var progressInterval = setInterval(updateProgress, interval);
    }

  //第二个进度条
var is_hand = 0;
var progressInterval1; // 将 progressInterval 定义在外部，以便全局访问

function simulateProgress1() {
    var progressBar = document.getElementById("myProgressBar1");
    var progressText1 = document.getElementById("progressText1");

    var height = 0;
    var duration = 2000; // 5秒
    var interval = 50; // 更新间隔

    var increment = (interval / duration) * 100;

    function updateProgress() {
        if (height >= 100) {
            clearInterval(progressInterval1);
        } else {
            if (is_hand === 1) {
                height += increment;
                progressBar.style.height = height + "%";
                progressText1.innerHTML = Math.round(height) + "%";
                //requestAnimationFrame(updateProgress); // 使用 requestAnimationFrame 更新
            } else {
                height=0;
                progressBar.style.height = height + "%";
                progressText1.innerHTML = Math.round(height) + "%";
                //requestAnimationFrame(updateProgress); // 使用 requestAnimationFrame 更新
            }
        }
    }


    progressInterval1 = setInterval(updateProgress, interval);
}

// 示例：在 is_hand 从 0 变为 1 时开始运行进度条
//is_hand = 0;
//simulateProgress1();


//  var is_hand = 1;
//  function simulateProgress1() {
//        var progressBar = document.getElementById("myProgressBar1");
//        var progressText1 = document.getElementById("progressText1");
//
//        var height = 1;
//        var duration = 5000; // 8秒
//        var interval = 10; // 更新间隔
//
//        var increment = (interval / duration) * 100;
//
//        var updateProgress = function () {
//            if (height >= 100) {
//                clearInterval(progressInterval);
//            } else {
//                if(is_hand === 1){
//                    height += increment;
//                    progressBar.style.height = height + "%";
//                    progressText1.innerHTML = Math.round(height) + "%";
//                 }
//                 else{
//                    height = 0;
//                    progressBar.style.height = '0';
//                    clearInterval(progressInterval);
//                 }
//            }
//        };
//
//        var progressInterval = setInterval(updateProgress, interval);
//    }


        var error_count = 0;
        var vision = 0.0;
        var mediapipeDirection = 0;
        var E_direction = 1;
        var flag = false; //判断标志位
        var shouldExit = false; // 周期函数结束标志位

          // 使用Fetch API 发起GET请求
          function updateLetterDirection() {
            var letterE = document.getElementById("vision-test");

            // 映射mediapipe返回的方向到字母 E 的方向
            var directionMap = {
                1: "rotate(0deg)",    // 右
                2: "rotate(90deg)",  // 下
                3: "rotate(180deg)",  // 左
                4: "rotate(270deg)"    // 上
            };


            // 判断方向是否正确,正确则修改修改方向
            console.log("media:", typeof mediapipeDirection, mediapipeDirection);
            console.log("E:", typeof E_direction, E_direction);
            var answer = 0;
            var distance = 80;
            if (mediapipeDirection === E_direction){
                answer = 1;
            }
            else{
                error_count += 1;
            }

            if(error_count >= 2){
                shouldExit = true;
                fetch('/api/close')
        .then(response=>{
        alert("视力评估结束！");})
        .catch(error => console.error('Error:', error));

            }
            var dataToSend = {
                "distance":distance,
                "answer":answer
            }

            if (mediapipeDirection === E_direction) {
                //改变E的方向
                fetch('/api/angle')
                .then(response => response.json())
                .then(data => {
                // 在这里使用返回的角度来改变字母E的方向
                const dynamicLetter = document.getElementById('vision-test');
                E_direction = data.rotation_angle;
                dynamicLetter.style.transform = directionMap[E_direction];
                //dynamicLetter.style.transform = `rotate(${data.rotation_angle}deg)`;
        })
        .catch(error => console.error('Error fetching angle:', error));
            }
        }

        //根据捕捉的食指方向
        var intervalId
        var pre_time = new Date();
        var end_time = new Date();
        var temp = -1;

        var directionCount = {
            1: 0,
            2: 0,
            3: 0,
            4: 0
        }

//        simulateProgress();

        simulateProgress1();

        intervalId = setInterval(function () {
        console.log('exit:',shouldExit);

             fetch('/api/mediapipedirection')
                .then(response => response.json())
                .then(data => {
                temp = data.direction;
                //没有检测到手,清空检测手的进度条
                if(temp === 0){
                    is_hand = 0;
                }
                else{
                    is_hand = 1;
                    directionCount[temp] += 1;
                }
              })
             .catch(error => console.error('Error fetching direction:', error));

            end_time = new Date();
            if(end_time - pre_time >= 5000 && !shouldExit){
                pre_time = end_time;
                //以5秒内出现次数最多的方向为此次食指的方向
                temp = Object.keys(directionCount).reduce((a, b) => directionCount[a] > directionCount[b] ? a : b);
                mediapipeDirection = parseInt(temp, 10);
                //字典值清零
                directionCount[1] = 0;
                directionCount[2] = 0;
                directionCount[3] = 0;
                directionCount[4] = 0;
                updateLetterDirection();

//                simulateProgress();
                clearInterval(progressInterval1);
                simulateProgress1();
                handleShouldExit();
             }

        }, 50); // 50ms更新一次方向


        var exitEvent = new Event('exitEvent');
// 在适当的时候触发事件
        function handleShouldExit() {
            if (shouldExit) {
                document.dispatchEvent(exitEvent);
            }
        }

        // 使用事件监听器监听事件
        document.addEventListener('exitEvent', function() {
            clearInterval(intervalId);
            clearInterval(progressInterval1);
            console.log('周期函数结束');
        });
