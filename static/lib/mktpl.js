require("../../../../bower_components/zepto/zepto.js");

window.$frash = {};

(function(){
    var $body;
    var delimiters_left = '<$';
    var delimiters_right = '$>';
    var exchange = function(ele, source) {
        if(ele.attr("bind") != undefined) {
            var word = ele.attr("bind");
            var words = word.split(".");
            iterator = words[0];
            key = words[1];
            ele.html(source[key]);    
        }
        ele.children().each(function(){
            exchange($(this), source);
        });
    };
    var source_result = function(s,words ,i,fun) {
        // console.log(s[words[i]]);
        // console.log(words[i]);
        if(typeof(s[words[i]]) != 'object') {
            fun(s[words[i]]);
        }
        else {

            source_result(s[words[i]],words, i+1,fun);
        }
        
    };
    var exchange_attr = function(ele , source) {
        html = ele.html();
        attrs = html.split(delimiters_left);
        fin_html = "";
        for(i in attrs) {
            attr = attrs[i];
            if(attr.indexOf(delimiters_right) != -1) {
                la = attr.split(delimiters_right);
                words = la[0].split(".");
                // console.log(words);
                // console.log(source[words[1]]);
                //console.log(source_result(source ,words ,1));
                source_result(source ,words ,1,function(html){
                    fin_html += html + la[1];
                    //alert(fin_html);
                });
                // console.log(fin_html);
            }
            else {
                fin_html += attr;
            }
        }
        ele.html(fin_html);
    };
    var fill_template = function(tag_ele, source) {
        var wrap = tag_ele.parent();
        copy_ele = tag_ele;
        copy_ele.attr("repeated",true);
        wrap.html("");
        wrap = wrap.append(copy_ele.clone());
        if(copy_ele.attr("tpl") == "true") {
            copy_ele.removeAttr("tpl");
            copy_ele.removeClass("tpl");
        }
        if(source.length == 0) {
            c = copy_ele.clone();
            wrap = wrap.append(c);
            c.addClass("hidden");
        }
        else {
            for(i in source) {
                c = copy_ele.clone();
                wrap = wrap.append(c);
                exchange(c,source[i]);
                exchange_attr(c,source[i]);
                if(c.hasClass("hidden")) {
                    c.removeClass("hidden");
                }
            }
        }
    };
    var compile_repeat = function(tag_ele) {
        var word = tag_ele.attr("repeat").split(" ");
        data = {};
        if(word.length == 3) {
            if(word[1] != 'in') {
                console.error("template syntax error");
            }
            else {
                data.iterator = word[0];
                data.source = word[2];
                for(i in $frash) {
                    // console.log(i);
                    // console.log(data.source);

                    if($frash[i] != undefined && data.source == i) {
                        fill_template(tag_ele,$frash[i]);
                        //console.log('sdf' + $frash[i]);
                    }
                }
            }
        }
        else {
            console.error("template syntax error");
        }
    };
    var remove_repeat = function(tag_ele) {
        ele = tag_ele;
        if(ele.next().attr("repeated") != undefined && ele.attr("repeat") == ele.next().attr("repeat")) {
            ele.next().remove();
            remove_repeat(ele);
        }
        if(ele.next().attr("repeated") == undefined) {
            ele.removeAttr("repeated");
            compile_repeat(ele);
        }
        ele.remove();
    };
    var refrashed = 0;
    var deep_search = function(ele) {
        var childrens = ele.children();
        childrens.each(function(){
            if ($(this).attr("repeat") != undefined && $(this).attr("repeated") == undefined) {
                $(this).attr("tpl","true");
                $(this).addClass("tpl");
                compile_repeat($(this));
            }
            else if($(this).attr("repeat") != undefined && $(this).attr("repeated") == "true") {
                remove_repeat($(this));
            }
            deep_search($(this));
        });
    };
    $frash.$apply = function() {
        if($body == undefined) {
            $body = $("body");
            deep_search($body);
        }
        else {
            deep_search($body);
        }
    };
})();
