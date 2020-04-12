var myapp = angular.module("warren", []);
var host = "http://gabrieluribe.me:5000/";
var buyHost = "http://localhost:5000/stocks/buy";
var sellHost = "http://localhost:5000/stocks/sell";
var testHost = "http://localhost:5000/stocks/";
var test = "http://localhost:5000/stocks/";
myapp.config(['$httpProvider', function ($httpProvider) {
    $httpProvider.defaults.headers.post['Content-Type'] = 'application/x-www-form-urlencoded; charset=UTF-8';
}]);
console.log("in app.js");
myapp.controller("mainController", function ($scope, $http, $interval) {

    //sample data
    //$scope.stocks = [{"symbol": "Fincad", "price": 5}, {"sybmol": "Microsoft", "price": 4}, {"sybmol": "Google", "price": 3},
    //                {"sybmol": "AppNeta", "price": 5}];

    //start polling data from the service
    $scope.myData = [1,2,28,4,5];
    $scope.money=10000;
    $scope.test="hello";
    $http({
        url: test+"all",
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
    
    $scope.buy = function (symbol) {
        debugger;
        $http({
            url: buyHost,
            method: "POST",
            data:"symbol="+symbol
        }).then(function successCallback(response) {
            console.log(response.data);
            debugger
                $scope.money=response.data;

            // this callbalsck will be called asynchronously
            // when the response is available
        }, function errorCallback(response) {
            console.log(response);
            // called asynchronously if an error occurs
            // or server returns response with an error status.
        });
    };
    $scope.sell = function (symbol) {

        $http({
            url: sellHost,
            method: "POST",
            data:"symbol="+symbol
        }).then(function successCallback(response) {
            console.log(response.data);
            debugger
            $scope.money=response.data;
            // this callbalsck will be called asynchronously
            // when the response is available
        }, function errorCallback(response) {
            console.log(response);
            // called asynchronously if an error occurs
            // or server returns response with an error status.
        });
    };
    $scope.proforio=function () {
        $http({
            url: "http://localhost:5000/user/portfolio",
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
    }
    
    $scope.home=function () {
        console.log("in home function");
        $http({
            url: test+"all",
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
    }

});
