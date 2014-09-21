var app = angular.module('rememberall', []).config(function($sceDelegateProvider) {
      $sceDelegateProvider.resourceUrlWhitelist([
          'self',
          'http://localhost:5000/**'
      ]);
});

app.controller('MainPanelCtrl', function($scope, $rootScope, 
                                         testDataFactory, JournalViewFactory) {
  $scope.journal = testDataFactory.journal;

  $scope.coverStyle = function(fileURL) {
    if(!(typeof fileURL === 'undefined')) {
      return {
        'background-image': 'url(' + fileURL + ')',
        'background-size': 'cover'
      };
    }
  };

  $scope.open = function(entry) {
    JournalViewFactory.visible = true;
    $rootScope.currentEntry = entry;
  };

  $scope.hasThumbnail = function(url) {
    return !(typeof url === 'undefined');
  };

  $scope.openEntry = function() {
    return JournalViewFactory.visible;
  };
});

app.controller('JournalCtrl', function($scope, $rootScope, savedFactory, JournalViewFactory) {
  $scope.openEntry = function() {
    return JournalViewFactory.visible;
  };
  $scope.close = function() {
    JournalViewFactory.visible = false;
  };
  $scope.currentEntry = function() {
    return $rootScope.currentEntry;
  };
  $scope.getSaved = function() {
    return savedFactory.saved;
  };
});

app.controller('RememberAllCtrl', function($scope) {
  $scope.currentEntry = {};
});

app.factory('JournalViewFactory', function() {
  return {
    visible: false,
  };
});

app.controller('SideBarCtrl', function($scope, $http, searchResultsFactory, savedFactory) {
  $scope.searchResults = searchResultsFactory.results;

  $scope.editor = function(clipUrl) {
    editorFactory.isVisible = true;
    editorFactory.openedClip = clipUrl;
  }; 
  $scope.getSaved = function() {
    return savedFactory.saved;
  };

  var client = new elasticsearch.Client({
    host: 'localhost:9200',
    log: 'trace'
  });

  $scope.saveDialog = '';
  $scope.modalOpen = false;
  $scope.saveClip = function(clipURL) {
    console.log('saving clip at url ' + clipURL)
    $scope.saveDialog = clipURL;
    $scope.modalOpen = true;
  };
  $scope.showModal = function() {
    return $scope.modalOpen;
  };
  $scope.clickModalSave = function() {
    console.log('saving ' + $scope.saveDialog);
    console.log('title: ' + $scope.title);
    savedFactory.saved.push({title: $scope.title, url: $scope.saveDialog});
    $scope.title = '';
    $scope.saveDialog = '';
    $scope.modalOpen = false;
  }; 
  $scope.clickModalCancel = function() {
    $scope.saveDialog = '';
      $scope.modalOpen = false;
  };
 
  $scope.searchClicked = function(keywordString, timeString) {
    var tildaString = keywordString.replace(/\s/g, "~ ") + '~';
   
    client.search({
      index: 'rememberall',
      type: 'frame',
      body: {
        query: {
          query_string: {
            query: tildaString
          }
        }
      }
    }).then(function(resp) {
      var hits = resp.hits.hits;
      res = [];
      for (var i = 0; i < hits.length; i++) {
          var fileName = hits[i]['_source']['filename'];
          var url = 'http://localhost:5000/static/data/' + fileName;
          res.push({thumbnail: null, video: url});
      }
      $scope.searchResults = res;
      console.log($scope.searchResults);
      $scope.$apply();
    }, function(err) {
      console.trace(err.message);
    });

    /*var url = ''; // TODO Build with keywordString and timeString.
    $http.get(url).success(function(response) {
      // TODO processing before saving, maybe?
      searchResultsFactory.results = response;
      $scope.searchResults = response;
    });*/
  };
});

app.factory('savedFactory', function() {
  return {
    saved: [] 
  };
});

app.factory('searchResultsFactory', function() {
  return {
    results: [] 
  };
});

app.factory('testDataFactory', function() {
  return { 
    journal: [
      {title: 'Anish Hard at Work', date: 'September 20, 2014 11:35', 
       thumbnail: '../media/photo.JPG',
       content: [{type: 'video', value: '../media/clip.mp4'}, {type: 'text', value: 'Collaboratively administrate empowered markets via plug-and-play networks. Dynamically procrastinate B2C users after installed base benefits. Dramatically visualize customer directed convergence without revolutionary ROI.'}]},
        {title: 'Moaaz Joins the Team', thumbnail: '../media/photo2.JPG', 
       date: 'September 19, 2014 23:37',
       content: [{type: 'text', value: 'We only had 3 team members...'},
                 {type: 'video', value: '../media/clip2.mp4'}, 
                 {type: 'text', value: "Hack the North is Canada's premier hackathon. It's an event where 1,000 students with different technical backgrounds and skill levels will come together, for 36 hours, form teams around a problem or idea, and collaboratively code a unique solution from scratch. With world class mentors, food, and hardware resources, you're in for an amazing time!"}]},
      {title: 'Arrival at University of Waterloo', date: 'September 19, 2014 20:50',
       thumbnail: '../media/photo3.png'},
      {title: 'Chillin at YYZ', time: 'September 19, 2014 19:01', content: [
        {type: 'text', value: 'The security at customs is so intense. And terrifying. I walked up to the counter to hand my passport and froze. The guy was huge to begin with. And then someone had the great idea to put a great old vest on him. I handed him my papers. He asked why I was coming to Canada. My voice did the thing it does when my mind has decided to ride in the back seat. It was like tissue paper. Visible, but on the edge of vanishing.'}]},
      {title: 'On the Way to the Airport', date: 'September 19, 2014 14:14',
       thumbnail: '../media/photo4.jpg'},
      {title: 'Packing List', content: [{type: 'text',
                                   value: 'One towel, six tshirts (got to be prepared), two pairs of flip-flops: one fuzzy, one not, socks, an extra pair of jeans, two jackets, a scarf, a mug, a strainer, Earl\'s Garden tea, and Google glass.'}]},
    ]
  };
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

app.directive('journal', function() {
  return {
    restrict: 'E',
    templateUrl: '../partials/journal.partial.html'
  };
});
