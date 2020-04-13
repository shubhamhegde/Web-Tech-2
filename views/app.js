        
        myapp=angular.module("warren", ["zingchart-angularjs"]);

        myapp.service('Username',[function(){
            self=this;

            var username="MM";
            var assign=function(name){
                username=(name);
                console.log("in assign");
                console.log(username);
            };
            var getname=function(){
                console.log("in get");
                console.log(username);
                return username;
            };
            return {assign: assign,
                getname:getname};
        }]);

        myapp.controller("mainController", ["$http","$scope","$rootScope","$window","Username",function ($http,$scope,$rootScope,$window,Username) {
            self=this;

            console.log("start");
            $scope.username;
            
            
            /*
            self.changeName=function(){
                Username.username=$scope.username;
                console.log("in boradcast",Username.username)
                $rootScope.$broadcast('MAIN_SERVICE_VALUE_CHANGED');
            }*/
                        //$scope.addname = function() {
                //
            //};
            

            $scope.money=10000;
            $scope.test="hello";
            $http({
                url: "http://localhost:5000/stocks/all",
                method: "GET"
            }).then(function successCallback(response) {
            console.log(response.data);
            $scope.stocks=response.data;
            // this callbalsck will be called asynchronously
            // when the response is available
            }, function errorCallback(response) {
                    console.log(response);
            // called asynchronously if an error occurs
            // or server returns response with an error status.
            });
            
            self.disable=function(){
                if($scope.user){
                    console.log("enable");
                }
                else{
                    console.log("disable");
                    $('#buy').attr('disabled',true);
                    $('#sell').attr('disabled',true);
                }
            };

            $http({
                url: "http://localhost:5000/api/user",
                method: "GET"
            }).then(function successCallback(response) {
            console.log(response.data);
            $scope.user=response.data["uname"];
            console.log($scope.user);
            $scope.money=parseFloat(response.data["amount"]);
            // this callbalsck will be called asynchronously
            // when the response is available
            }, function errorCallback(response) {
                    console.log(response);
            // called asynchronously if an error occurs
            // or server returns response with an error status.
            });
            
            $window.sessionStorage.setItem("username",$scope.user);

            $scope.user=$window.sessionStorage.getItem("username");


            self.home=function(){
                
                console.log("in home");
                 $http.get(
                     "http://localhost:5000/stocks/all"                    
                    ).then(function successCallback(response) {
                    console.log(response.data);
                    $scope.stocks=response.data;
            // this callbalsck will be called asynchronously
            // when the response is available
                    }, function errorCallback(response) {
                    console.log(response);
            // called asynchronously if an error occurs
            // or server returns response with an error status.
                });
            };

            self.buy = function (symbol) {
                    //debugger;

                    console.log("in buy");
                    //data="{'symbol':"+symbol+"}";
                    data="{\"symbol\":\""+symbol+"\",\"username\":\""+$scope.user+"\"}";
                    console.log(data);
                    if($scope.user){
                    $http({
                        url: "http://localhost:5000/stocks/buy",
                        method:"POST",
                        data:JSON.parse(data),
                        headers: {'Content-Type': 'application/json' }
                    
                    }).then(function successCallback(response) {
                        console.log(response.data);
                        //debugger;
                        $scope.money=response.data;

                    // this callbalsck will be called asynchronously
                    // when the response is available
                    }, function errorCallback(response) {
                    console.log(response);
                    // called asynchronously if an error occurs
                    // or server returns response with an error status.
                });}
                else{this.alert("Please login");
                    return false;}
            };

            self.detail = function(symbol){
                    console.log("in detail");
                    data="{'symbol':"+symbol+"}";
                    console.log(data);

                    $http({
                        url: "http://localhost:5000/stocks/detail",
                        method:"POST",
                        data:JSON.stringify(data),
                        headers: {'Content-Type': 'application/json' }
                    
                    }).then(function successCallback(response) {
                        console.log(response.data);
                        //debugger;
                        var a=response.data["actual"];
                        var p=response.data["predict"];
                        console.log(a);
                        console.log(p);
                        $scope.myData={  
                            type: "line", 

                            label: [
                                {
                                    text: "Open_price:<br>%plot-0-value",
                                    'default-value': "__",
                                    x: "15%",
                                    y: "7%",
                                    'background-color': "blue ",
                                    'font-family': "Georgia",
                                    'font-color': "white",
                                    'font-size':14,
                                    height: "15%",
                                    width: "10%",
                                    'border-radius': "5px"
                                },
                                {
                                  text: "Red:<br>%plot-1-value",
                                  'default-value': "__",
                                  x: "30%",
                                  y: "7%",
                                  'background-color': "red #D31E1E",
                                  'font-family': "Georgia",
                                  'font-color': "white",
                                  'font-size':14,
                                  height: "15%",
                                  width: "10%",
                                  'border-radius': "5px"
                                }],

                            scaleX: {
                                transform: {  
                                    type: 'date'  ,
                                    all: '%m/%d/%y '  
                                    }
                                }, 

                            series: [  
                                {  
                                    values : a  ,
                                    "line-color":"blue"  
                                },
                                {
                                    values:  p    ,
                                    "line-color":"red"
                                } 
                            ],
                        };

                    // this callbalsck will be called asynchronously
                    // when the response is available
                    }, function errorCallback(response) {
                    console.log(response);
                    // called asynchronously if an error occurs
                    // or server returns response with an error status.
                });
            };

            self.sell = function(symbol){
                    console.log("in sell");
                    //data="{'symbol':"+symbol+"}";
                    data="{\"symbol\":\""+symbol+"\",\"username\":\""+$scope.user+"\"}";
                    console.log(data);
                    if($scope.user){
                    $http({
                        url: "http://localhost:5000/stocks/sell",
                        method:"POST",
                        data:JSON.parse(data),
                        headers: {'Content-Type': 'application/json' }
                    
                    }).then(function successCallback(response) {
                        console.log(response.data);
                        //debugger;
                        if("status" in response.data)
                            alert("Error! You have not purchased stocks in this company. Try with another company.")
                        else
                            $scope.money=response.data["status1"];
                        

                    // this callbalsck will be called asynchronously
                    // when the response is available
                    }, function errorCallback(response) {
                    console.log(response);
                    // called asynchronously if an error occurs
                    // or server returns response with an error status.
                });
            }
            else{
                alert("Please login");
                return false;
            }
            };

        self.login = function(){
                console.log("login");
                var landingUrl = "login.html";
                $window.location.href = landingUrl;
        };

        self.signup = function(){
                console.log("signup");
                var landingUrl = "signup.html";
                $window.location.href = landingUrl;
        };

        self.logout = function(){
                console.log("logout");
                $http({
                    url: "http://localhost:5000/api/logout",
                    method: "GET"
            }).then(function successCallback(response) {
                console.log(response.data);
                $scope.user=response.data["uname"];
                $scope.money=parseFloat(response.data["amount"]);
            }, function errorCallback(response) {
                    console.log(response);
            });
        };

        self.proforio = function(){
            console.log("profile");
            if($scope.user){
                var landingUrl = "proforio.html";
                $window.location.href = landingUrl;
            }
            else{
                return false;
            }
        };
    
    }]);

myapp.controller("proforioCtrl",['$scope','$rootScope','$window','Username',function($scope,$rootScope,$window,Username){
    console.log("imhere");
    self=this;
    /*
    self.username=Username.username;
    $rootScope.$on('MAIN_SERVICE_VALUE_CHANGED',function(){
              self.username=Username.username;
              console.log("in root",self.username);
  
        });
   */
   self.username = $window.sessionStorage.getItem("username");

    console.log(self.username);
}])
    