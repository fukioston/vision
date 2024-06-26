var progressInterval;
var track_first_width = 0;
var root=document.documentElement;
var width = 1;
    function simulateProgress() {
        var progressBar = document.getElementById("myProgressBar");
        var progressText = document.getElementById("progressText");

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
                root.style.setProperty("--width",width + "%");
            }
        };

        progressInterval = setInterval(updateProgress, interval);
    }

  //第二个进度条
var is_hand = 0;
var track_second_height = 0;
var progressInterval1; // 将 progressInterval 定义在外部，以便全局访问
 var height = 0;
function simulateProgress1() {
    var progressBar = document.getElementById("myProgressBar1");
    var progressText1 = document.getElementById("progressText1");


    var duration = 2000; // 5秒
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
                root.style.setProperty("--height",(height*3) + "px") ;
                //requestAnimationFrame(updateProgress); // 使用 requestAnimationFrame 更新
            } else {
                height=0;
                track_second_height = height;
                root.style.setProperty("--height",0 + "px") ;
            }
        }
    }


    progressInterval1 = setInterval(updateProgress, interval);
}

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

        var the_last_gesture = 0;
        var error_count = 0;
        var vision = 0.0;
        var mediapipeDirection = 0;
        var pre_mediapipeDirection = 0;
        var E_direction =8;
        var flag = false; //判断标志位
        var shouldExit = false; // 周期函数结束标志位

          // 使用Fetch API 发起GET请求
          function updateLetterDirection() {
            var letterE = document.getElementById("vision-test");

            // 映射mediapipe返回的方向到字母 E 的方向
            var directionMap = {
                5: 5,    // 右
                6:6,  // 下
                8: 8,  // 左
                9: 9   // 上
            };



            // 判断方向是否正确,正确则修改修改方向

            if (mediapipeDirection === E_direction){
                answer = 1;

                root.style.setProperty('--color','green');
                root.style.setProperty('--backimage','none');
            }
            else{
                error_count += 1;

                root.style.setProperty('--color','red');
                root.style.setProperty('--backimage','none');
            }

            if(error_count >= 2){
                shouldExit = true;
                fetch('/api/close')
        .then(response=>{
        // alert("视力评估结束！");
            showSwal('success-message',"你的结果是"+score.toFixed(1)+",还要再来一次吗");
        clearInterval(progressInterval1);
        clearInterval(progressInterval);
             handleShouldExit();})
        .catch(error => console.error('Error:', error));

            }

            if (mediapipeDirection === E_direction) {
                //改变E的方向
                fetch('/api/number',{
                method: 'POST',
                headers: {
                'Content-Type': 'application/json'
        },
                body: JSON.stringify({
            value: E_direction
        }),
    })
                .then(response => response.json())
                .then(data => {
                    score+=0.1;
                    if(score>5.2)
                    {
                        shouldExit=true;
                        fetch('/api/close')
        .then(response=>{
        // alert("视力评估结束！");
            showSwal('success-message',"你的结果是"+score.toFixed(1)+",还要再来一次吗");
        clearInterval(progressInterval1);
        clearInterval(progressInterval);
             handleShouldExit();})
        .catch(error => console.error('Error:', error));
                        }


                var scoreDisplay = document.getElementById("score-display");
                scoreDisplay.innerText = "Score: " + score.toFixed(1);
                var fontSize = calculateFontSize(score);
                letterE.style.fontSize = fontSize + 'px';
                    E_direction = data.rand;
                    letterE.innerText=directionMap[data.rand]
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
           5: 0,
            6: 0,
            8: 0,
            9: 0,
            0:0,
        }

        intervalId = setInterval(function () {
             fetch('/api/mediapipedirection2')
                .then(response => response.json())
                .then(data => {
                temp = data.direction;

                //没有检测到手,清空检测手的进度条
                if(temp === 0){
                    is_hand = 0;

                }
                else{//检测到手
                    is_hand = 1;

                    the_last_gesture = temp;//记录当前手的姿势
                    if(the_last_gesture === pre_mediapipeDirection){//前后两次手的姿势相同
                         pre_mediapipeDirection = the_last_gesture;
                    }
                    else{//前后两次手的姿势不同
                         is_hand = 0;

                         pre_mediapipeDirection = the_last_gesture;
                    }
                }
              })
             .catch(error => console.error('Error fetching direction:', error));


            if(track_first_width >= 100 && !shouldExit){

                    track_first_width = 0;

                     width=1;height=0;
                    clearInterval(progressInterval1);
                    mediapipeDirection = the_last_gesture;
                    updateLetterDirection();
                    simulateProgress();
                    simulateProgress1();
                }
                else{
                if(track_second_height >= 100 &&!shouldExit){
                    track_second_height = 0;

                    width=1;height=0;
                   clearInterval(progressInterval);
                   mediapipeDirection = the_last_gesture;
                   updateLetterDirection();
                   simulateProgress();
                   simulateProgress1();
//
//
//                   handleShouldExit();


            }
                }

        }, 200); // 50ms更新一次方向


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

        });
