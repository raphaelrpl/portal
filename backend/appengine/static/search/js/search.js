var searchModule = angular.module('searchModule', ['rest']);

searchModule.directive('typeahead', function($timeout) {
    return {
        restrict: 'AEC',
        scope: {
            items: '=',
            urlreq: '@',
            prompt: '@',
            title: '@',
            subtitle: '@',
            model: '=',
            onSelect: '&'
        },
        controller: function($scope, $http) { // DI in action
            $scope.cleanField = function() {

            };
            $scope.dispatchSearch = function() {
                console.log("DISPACHANDO");
                $http.get($scope.urlreq).success(function (data) {
                    $scope.items = data;
                });
            };
            $scope.name = ''; // This will hold the selected item
            $scope.onItemSelected = function () { // this gets executed when an item is selected
                console.log('selected=' + $scope.name);
            };
        },
        link: function(scope, elem, attrs) {
            scope.handleSelection = function(selectedItem) {
                scope.model = selectedItem;
                console.log(scope.model);
                scope.current = 0;
                scope.selected = true;
                $timeout(function() {
                    scope.onSelect();
                }, 200);
            };
            scope.current = 0;
            scope.selected = true; // hides the list initially
            scope.isCurrent = function(index) {
                return scope.current == index;
            };
            scope.setCurrent = function(index) {
                scope.current = index;
            };
        },
        templateUrl: '/static/search/html/template.html'
    };
});