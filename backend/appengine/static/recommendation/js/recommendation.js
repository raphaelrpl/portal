var recommendationModule = angular.module("recommendationModule", []);

recommendationModule.directive("recommendButton", function() {
    return {
        restrict: 'E',
        replace: true,
        templateUrl: '/static/recommendation/html/button.html',
        scope: {
            post: '@'
        },
        controller: function($scope, $http) {
            $scope.already = false;
            $http.post("/recommend/check/"+$scope.post, {}).success(function(data) {
                $scope.already = data.status == 1;
            });

            $scope.doRecommend = function() {
                console.log("Recomendando o post : " + $scope.post);
                $http.post('/recommend/'+$scope.post, {}).success(function(data) {
                    console.log(data);
                    $scope.already = data.status == 1;
                }).error(function(errors) {
                    alert("Falha ao recomendar");
                });
            }
        }
    }
});