var progressInterval;
var begin = 0;
var track_first_width = 0;
    function simulateProgress() {
        var progressBar = document.getElementById("myProgressBar");
        var progressText = document.getElementById("progressText");

        var width = 1;
        var duration = 8000; // 8秒
        var interval = 10; // 更新间隔

        var increment = (interval / duration) * 100;

        var updateProgress = function () {
            if (width >= 100) {
                track_first_width = width;
                clearInterval(progressInterval);
            } else {
                width += increment;
                track_first_width = width;
                progressBar.style.width = width + "%";
                progressText.innerHTML = Math.round(width) + "%";
            }
        };

        progressInterval = setInterval(updateProgress, interval);
    }

  //第二个进度条
var is_hand = 0;
var track_second_height = 0;
var progressInterval1; // 将 progressInterval 定义在外部，以便全局访问

function simulateProgress1() {
    var progressBar = document.getElementById("myProgressBar1");
    var progressText1 = document.getElementById("progressText1");

    var height = 0;
    var duration = 3000; // 5秒
    var interval = 50; // 更新间隔

    var increment = (interval / duration) * 100;

    function updateProgress() {
        if (height >= 100) {
            track_second_height = height;
            clearInterval(progressInterval1);
        } else {
            if (is_hand === 1) {
                height += increment;
                track_second_height = height;
                progressBar.style.height = height + "%";
                progressText1.innerHTML = Math.round(height) + "%";
                //requestAnimationFrame(updateProgress); // 使用 requestAnimationFrame 更新
            } else {
                height=0;
                track_second_height = height;
                progressBar.style.height = height + "%";
                progressText1.innerHTML = Math.round(height) + "%";
                //requestAnimationFrame(updateProgress); // 使用 requestAnimationFrame 更新
            }
        }
    }


    progressInterval1 = setInterval(updateProgress, interval);
}

//在 is_hand 从 0 变为 1 时开始运行进度条
//is_hand = 0;
//simulateProgress1();

        var the_last_gesture = 0;
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
                    score+=0.1;
                var scoreDisplay = document.getElementById("score-display");
                scoreDisplay.innerText = "Score: " + score.toFixed(1);
                var fontSize = calculateFontSize(score);
                letterE.style.fontSize = fontSize + 'px';
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
        var ready=1;
        var directionCount = {
            1: 0,
            2: 0,
            3: 0,
            4: 0
        }

        console.log("begin",begin);


        //周期性地探测食指方向并检查进度条进度
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
                   the_last_gesture = temp;
                   directionCount[temp] += 1;
               }
             })
            .catch(error => console.error('Error fetching direction:', error));

            //食指方向保持时间已经满足
            if(track_second_height >= 100 && !shouldExit){
                console.log("蓝色进度条已满");
                pre_time = end_time;
                mediapipeDirection = the_last_gesture;

                 // clearInterval(intervalId);
                 updateLetterDirection();
                clearInterval(progressInterval);
                clearInterval(progressInterval1);

                simulateProgress1();
                handleShouldExit();
            }
            else{
                if(track_first_width >= 100 && !shouldExit){//超时
                    console.log("绿色进度条已满");
                    pre_time = end_time;
                    temp = Object.keys(directionCount).reduce((a, b) => directionCount[a] > directionCount[b] ? a : b);
                    mediapipeDirection = the_last_gesture;

                    //字典值清零
                    directionCount[1] = 0;
                    directionCount[2] = 0;
                    directionCount[3] = 0;
                    directionCount[4] = 0;
                    clearInterval(intervalId);
                    updateLetterDirection();

                    clearInterval(progressInterval1);
                    simulateProgress();
                    simulateProgress1();
                    handleShouldExit();
             }
            }

        }, 100); // 50ms更新一次方向


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
            clearInterval(progressInterval);
            clearInterval(progressInterval1);
            console.log('周期函数结束');
        });
