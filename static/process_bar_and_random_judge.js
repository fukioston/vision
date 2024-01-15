    function simulateProgress() {
        var progressBar = document.getElementById("myProgressBar");
        var progressText = document.getElementById("progressText");

        var width = 1;
        var duration = 5000; // 5秒
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
            var dataToSend = {
                "distance":distance,
                "answer":answer
            }

            fetch('/api/return', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(dataToSend),
                })
                .then(response => response.json())
                .then(data => {
                    if(data.exit === 1){
                        shouldExit = true;
                        alert(data.best_vision);
                    }
                    //console.log('Success:', data);
                })
                .catch((error) => { console.error('Error:', error);});


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
        var pre_time = new Date();
        var end_time = new Date();
        var temp = -1;

        var directionCount = {
            1: 0,
            2: 0,
            3: 0,
            4: 0
        }

        simulateProgress();
        setInterval(function () {
             fetch('/api/mediapipedirection')
                .then(response => response.json())
                .then(data => {
                temp = data.direction;
                directionCount[temp] += 1;
              })
             .catch(error => console.error('Error fetching direction:', error));
            end_time = new Date();
            if(end_time - pre_time >= 5000 && !shouldExit){
                pre_time = end_time;
                //以2秒内出现次数最多的方向为此次食指的方向
                temp = Object.keys(directionCount).reduce((a, b) => directionCount[a] > directionCount[b] ? a : b);
                mediapipeDirection = parseInt(temp, 10);
                //字典值清零
                directionCount[1] = 0;
                directionCount[2] = 0;
                directionCount[3] = 0;
                directionCount[4] = 0;
                updateLetterDirection();
                simulateProgress();
             }
        }, 50); // 50ms更新一次方向
