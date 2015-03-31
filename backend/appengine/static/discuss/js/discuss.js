/**
 * Created by raphael on 3/11/15.
 */

var discussModule = angular.module("discussModule", []);

discussModule.directive("discussform", function() {
    return {
        restrict: 'E',
        replace: true,
        templateUrl: '/static/discuss/html/discuss_form.html',
        scope: {
            discuss: '=',
            fileModel: '&'
        },
        controller: function($scope, $http) {
            $scope.errors = {};
            var formData = new FormData();
            $scope.prepareField = function(files) {
                formData.append("file", files[0]);
                //$scope.discuss.image = files[0];
            };
            $scope.publish = function() {
                var fd = new FormData();
                fd.append('file', $scope.myFile);

                //$http.post('/discusses/rest/new', formData, { withCredentials: true,
                //    headers: {'Content-Type': undefined },
                //    transformRequest: angular.identity
                //})
                $http.post('/discusses/rest/new', fd, {
                    transformRequest: angular.identity,
                    headers: {'Content-Type': undefined}
                }).success(function(discuss) {
                    console.log(discuss);
                }).error(function(errors) {
                    $scope.errors = errors;
                });
            }
        }
    }
});

discussModule.directive('fileModel', ['$parse', function ($parse) {
    return {
        restrict: 'A',
        link: function(scope, element, attrs) {
            var model = $parse(attrs.fileModel);
            var modelSetter = model.assign;

            element.bind('change', function(){
                scope.$apply(function(){
                    modelSetter(scope, element[0].files[0]);
                });
            });
        }
    };
}]);
//
//discussModule.directive("inputImage", ['$parse', function($parse){
//    return {
//        restrict: 'A',
//        link: function(scope, elm, attrs) {
//            elm.bind('change', function () {
//                $parse(attrs.inputImage).assign(scope, elm[0].files);
//                scope.$apply();
//            })
//        }
//    }
//}]);