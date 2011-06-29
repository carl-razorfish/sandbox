document.body.className = 'js';

RIA = {
    fn : {
        populateContainer : function(container,html) {
            var container = document.getElementById(container);
            container.innerHTML = html.join('');
        }
    },
    Class : {
        Article : function() {
            this.article = arguments[0];

            this.init = function() {
                this.feed = this.article.dataset['feed'];
                if (!this.feed) return;
                this.id = this.article.id;
                this.get();
            };
            this.get = function() {
                this.scpt = document.createElement('script');
                this.scpt.src = this.feed+'&callback='+this.id;
                document.body.appendChild(this.scpt);
            };
            this.init();
        }
    }
};

(function() {
    var articles = document.querySelectorAll('article[data-feed]');
    for (var i=0,article; article=articles[i]; i++) {
        new RIA.Class.Article(article);
    }
})();

function weather(data) {
    var html = [];
    html.push('<h3>'+data.query.results.channel.description+'</h3>');
    html.push('<p>'+data.query.results.channel.item.description+'</p>');
    RIA.fn.populateContainer('weather',html);
}

function news(data) {
    var html = [];
    var items = data.response.results;
    for (var i=0,item; item=items[i]; i++) {
        html.push('<h3><a href="'+item.webUrl+'" rel="external">'+item.fields.headline+'</a></h3>'+item.fields.trailText);
    }
    RIA.fn.populateContainer('news',html);
}
