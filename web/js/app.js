var app = angular.module('rememberall', []);

app.controller('MainPanelCtrl', function($scope) {
  $scope.value = 0;
});

app.controller('SideBarCtrl', function($scope) {
  $scope.feeling = 'happy';
});


app.directive('mainpanel', function() {
  return {
    restrict: 'E',
    templateUrl: '../partials/mainPanel.partial.html'
  };
});

app.directive('sidebar', function() {
  return {
    restrict: 'E',
    templateUrl: '../partials/sideBar.partial.html'
  };
});
