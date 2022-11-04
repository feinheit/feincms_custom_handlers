// https://gist.github.com/854622

// customized

    $.fn.close = function(){
        $(this).each(function(){
            var $this = $(this);
            log('closing ' + $this.attr('title'));
            $this.removeClass('mark');
            if (!$this.hasClass('nav-level-1')){
                $this.next().slideUp(500, function(){
                    $(this).addClass('closed');
                });
            }
        });
        return $(this);
    };

    $.fn.open = function(){
        log($(this));
        $(this).each(function(){
            var $this = $(this);
            log('opening '+ $this.attr('title'));
            $this.addClass('mark').next().slideDown(500, function(){
                    $.scrollTo($(this), 500);
                }).removeClass('closed');
        });
        return $(this);
    };


(function(window,undefined){

    // Prepare our Variables
    var
        History = window.History,
        $ = window.jQuery,
        document = window.document;

    // Check to see if History.js is enabled for our Browser
    if ( !History.enabled ) {
        return false;
    }

    // Wait for Document
    $(function(){
        // Prepare Variables
        var
            /* Application Specific Variables */
            contentSelector = '#content, article:first,.article:first,.post:first',
            $content = $(contentSelector).filter(':first'),
            contentNode = $content.get(0),
            $menu = $('#nav'),
            activeClass = 'mark active',
            activeSelector = '.mark, .active,.selected,.current',
            menuChildrenSelector = '.nav-level-1, .nav-level-2',
            /* Application Generic Variables */
            $body = $(document.body),
            rootUrl = History.getRootUrl(),
            scrollOptions = {
                duration: 800,
                easing:'swing'
            };

        // Ensure Content
        if ( $content.length === 0 ) {
            $content = $body;
        }

        // Internal Helper
        $.expr[':'].internal = function(obj, index, meta, stack){
            // Prepare
            var
                $this = $(obj),
                url = $this.attr('href')||'',
                isInternalLink;

            // Check link
            isInternalLink = url.substring(0,rootUrl.length) === rootUrl || url.indexOf(':') === -1;

            // Ignore or Keep
            return isInternalLink;
        };

        // HTML Helper
        var documentHtml = function(html){
            // Prepare

            var result = String(html)
                .replace(/<\!DOCTYPE[^>]*>/i, '')
                .replace(/<(html|head|body|title|meta|script)([\s\>])/gi,'<div class="document-$1"$2')
                .replace(/<\/(html|head|body|title|meta|script)\>/gi,'</div>')
            ;

            // Return
            return result;
        };

        // Ajaxify Helper
        $.fn.ajaxify = function(){
            // Prepare
            var $this = $(this);

            // Ajaxify
            $this.find('a:internal:not(.no-ajaxy)').click(function(event){
                // Prepare
                log('ajax-link');
                var
                    $this = $(this),
                    url = $this.attr('href'),
                    title = $this.attr('title')||null;

                // Continue as normal for cmd clicks etc
                if ( event.which == 2 || event.metaKey ) { log('no-ajax'); return true; }

                // Ajaxify this link
                History.pushState(null,title,url);
                event.preventDefault();
                return false;
            });

            // Chain
            return $this;
        };

        // Ajaxify our Internal Links
        $body.ajaxify();

        // Hook into State Changes
        $(window).bind('statechange',function(){
            // Prepare Variables
            var
                State = History.getState(),
                url = State.url,
                relativeUrl = url.replace(rootUrl,'');

            // Set Loading
            $body.addClass('loading');

            // Start Fade Out
            // Animating to opacity to 0 still keeps the element's height intact
            // Which prevents that annoying pop bang issue when loading in new content
            $content.animate({opacity:0},800);

            // Ajax Request the Traditional Page
            $.ajax({
                url: url,
                success: function(data, textStatus, jqXHR){
                    // Prepare
                    var
                        $data = $(documentHtml(data)),
                        $dataBody = $data.filter('.document-body:first'),
                        $dataContent = $dataBody.find('#content'),
                        $dataId = $dataContent.data('id'),
                        $menuChildren, contentHtml, $scripts, $links;

                    // Fetch the scripts
                    $scripts = $dataBody.find('.document-script');
                    if ( $scripts.length ) {
                        $scripts.detach();
                    }

                    // Fetch the css
                    $links = $data.find('link');
                    if ( $links.length ) {
                        $links.detach();
                    }

                    // Fetch the content
                    contentHtml = $dataContent.html()||$data.html();
                    if ( !contentHtml ) {
                        log('no content html. Redirecting...');
                        document.location.href = url;
                        return false;
                    }

                    // Update the menu
                    $menuChildren = $menu.find(menuChildrenSelector);
                    $menuChildren.filter(activeSelector).close(); //.removeClass(activeClass).change();
                    $menuChildren = $menuChildren.filter('[href^="/'+relativeUrl+'"]');
                    if ( $menuChildren.length === 1 ) {
                        $menuChildren.open();
                        }

                    // Update the content
                    $content.stop(true,true);
                    $content.data('id', $dataId);
                    $content.html(contentHtml).ajaxify().move(); /* you could fade in here if you'd like */

                    // Update the title
                    document.title = $dataContent.data('title');
                    try {
                        document.getElementsByTagName('title')[0].innerHTML = document.title.replace('<','&lt;').replace('>','&gt;').replace(' & ',' &amp; ');
                    }
                    catch ( Exception ) { }

                    // Add the scripts
                    $scripts.each(function(){
                        var $script = $(this);
                        if ($script.attr('src')) {
                            $.getScript($script.attr('src'));
                        } else {
                            var scriptText = $script.html(),
                            scriptNode = document.createElement('script');
                            scriptNode.appendChild(document.createTextNode(scriptText));
                            contentNode.appendChild(scriptNode);
                        }

                    });

                    // Add the CSS
                    $links.each(function(){
                        var $link = $(this);

                        var cssLink = $('<link />');
                            cssLink.attr({
                            "rel": $link.attr('rel'),
                            "type": $link.attr('type'),
                            "href": $link.attr('href')
                            });
                        $('head').append(cssLink);
                    });

                    // Complete the change
                    // if ( $body.ScrollTo||false ) { $body.ScrollTo(scrollOptions); } /* http://balupton.com/projects/jquery-scrollto */
                    $body.removeClass('loading');

                    // Inform Google Analytics of the change
                    if ( typeof window.pageTracker !== 'undefined' ) {
                        window.pageTracker._trackPageview(relativeUrl);
                    }

                    // Inform ReInvigorate of a state change
                    if ( typeof window.reinvigorate !== 'undefined' && typeof window.reinvigorate.ajax_track !== 'undefined' ) {
                        reinvigorate.ajax_track(url);
                        // ^ we use the full url here as that is what reinvigorate supports
                    }


                },
                error: function(jqXHR, textStatus, errorThrown){
                    document.location.href = url;
                    return false;
                }
            }); // end ajax

        }); // end onStateChange

    }); // end onDomLoad

})(window); // end closure
