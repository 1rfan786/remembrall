var app = angular.module('rememberall', []);

app.controller('MainPanelCtrl', function($scope) {
  $scope.value = 0;
});

app.controller('SideBarCtrl', function($scope) {
  $scope.feeling = 'happy';
});


app.directive('main-panel', function() {
  return {
    restrict: 'E',
    templateUrl: '../mainPanel.partial.html'
  };
});

app.directive('side-bar', function() {
  return {
    restrict: 'E',
    templateUrl: '../sideBar.partial.html'
  };
});
