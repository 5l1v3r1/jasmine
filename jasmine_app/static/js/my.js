$(function () {
    var Video = Backbone.Model.extend({
        defaults:
            {
                url: "",
                title: "",
                published_time: "",
                video_length: "",
                favorite_nums: "",
                comments_nums: "",
                points: "",
                level: "",
            },
        toggle: function () {
        }
    });
    var VideoList = Backbone.Collection.extend({
        url: "api/videos",
        model: Video,
    });
    var VideoView = Backbone.View.extend({
        tagName: "div",
        //在每个video的外层添加video-container
        className:"video-container",
        template: _.template($('#videoTemplate').html()),
        events: {
            "dbclick ": "close_video",
        },
        close_video: function () {
            alert("video should be closed")
        },
        initialize: function () {
        },
        render: function () {
            this.$el.html(this.template(this.model.toJSON()));
            return this;
        },
    });

    var VideoListView = Backbone.View.extend({
        el: "#videos",
        initialize: function () {
            this.collection = new VideoList();
            this.listenTo(this.collection, 'add', this.addOne);
            this.collection.fetch();
            this.render();
        },
        addOne:function(video){
            console.log(video);
            var video_view=new VideoView({model:video});
            this.$el.append(video_view.render().el);
        },
        render: function () {
        },
        renderVideo: function (item) {
            var videoView = new VideoView({
                model: item
            });
            this.$el.append(videoView.render().el);
        }
    });
    // 自动从服务端get数据
    var video_list_view = new VideoListView();


});
