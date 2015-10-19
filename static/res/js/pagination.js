/*
 *  Project:	Pagination
 *  Description:	a Plugin for creating page numbers
 *  Author:		
 *  License:	v1.0
 */
;(function ( $, window, document, undefined ) {
    // Create the defaults once
    var pluginName = "Pagination",
        defaults = {
            pagerName: "pager",			//分页的容器
			viewCount: 5,				//可显示多少条数据
			dataCount: 0,				//如果后台取数据，总数多少（静态的不用）
			selectClass: "selectno",			//选中的样式

			listCount:10,				//显示多少个分页码（不包括前一页，后一页）
			enablePrevNext:true,		//允许显示前一页后一页
			enableFirst:true,			//允许只有一页的情况下显示页码
			template:"default",			//模板（现只有default）
			
			mode:"static",				//"url" or "ajax"
			urlparameter:"",		//url参数,后面aa=1&bb=2...
			urlbase:"",				//基准url，
			currentPage:1,			//当前页
			callback:null			//回调函数（ajax取数据或者静态也可以使用）
        };

    // The actual plugin constructor
    function Plugin( element, options ) {
        this.element = element;
        this.options = $.extend( {}, defaults, options );
        //this._defaults = defaults;
        this._name = pluginName;
        this.init();
    }
	
	//private
	//获取url参数
	var getQueryString = function (name) {
		var reg = new RegExp("(^|&)" + name + "=([^&]*)(&|$)", "i");
		var r = window.location.search.substr(1).match(reg);
		if (r != null) return unescape(r[2]); return undefined;
	}
	//静态模板数据展示
	var Bind_StaticData = function($content,minnum,maxnum) {
		if (minnum > 0) {
			$content.children(":gt(" + (minnum - 1) + "):lt(" + maxnum + ")").css("display", "block");
		} else {
			$content.children(":lt(" + maxnum + ")").css("display", "block");
		}
		$content.children(":lt(" + (minnum) + ")").css("display", "none");
		$content.children(":gt(" + (maxnum - 1) + ")").css("display", "none");	
	}
	
	//主要
	//创建SetPager类
	var SetPager = function (options,pageCount){
		this.op = options;
		this.pageCount = pageCount;
	}
	SetPager.prototype = {
		//格式化成a元素
		FormatStr : function(pageNo, pageText) {
			//修改URL拼接规则
			//var href = this.op.mode=='url'?location.pathname+"?"+this.op.urlparameter+"&page="+pageNo:"javascript:void(0);";
			//var href = this.op.mode=='url'?this.op.urlbase+"/page/"+pageNo:"javascript:void(0);";
			var href = "javascript:void(0);";
			if(this.op.mode=='url'){
				var pos = this.op.urlbase.indexOf('?');
				if(pos==-1)
					href = this.op.urlbase+"?"+"page="+pageNo;
				else if(pos==(this.op.urlbase.length-1))
					href = this.op.urlbase+"page="+pageNo;
				else{
					var pos2 = this.op.urlbase.indexOf('&');
					if(pos2==(this.op.urlbase.length-1))
						href = this.op.urlbase+"page="+pageNo;
					else
						href = this.op.urlbase+"&"+"page="+pageNo;
				}
			}			
			
			if (typeof (pageText) == "number") {
				return "<a href='"+href+"' >" + pageText + "</a>";
			}
			return "<a href='"+href+"' i='" + pageNo + "'>" + pageText + "</a>";
		},
		//选中状态a元素
		FormatStrIndex : function(pageNo){
			return "<span class='"+this.op.selectClass+"'>" + pageNo + "</span>";
		},	
		//默认模板初始化页码集合
		InitDefaultList : function(_pageIndex){
			if(this.op.listCount<5)
					throw new Error("listCount must be lager than 5");	//listCount>5
			var pageIndex = parseFloat(_pageIndex);		//转化为number
			var ns = new Array();
			var numList = new Array(this.op.listCount);	
			if (pageIndex >= this.op.listCount) {   
				numList[0] = 1;
				numList[1] = "…";	
				var infront = 0;
				var inback = 0;
				var inflag = Math.floor((this.op.listCount-2)/2);
				if(this.op.listCount%2==0){
					infront = inflag-1;
					inback = inflag;
				}else{
					infront = inflag;
					inback = inflag;
				}
				if (pageIndex + inback >= this.pageCount) {                
					for (i = this.pageCount - (this.op.listCount-3); i < this.pageCount + 1; i++) {
						ns.push(i);
					}
					for (j = 0; j <= (this.op.listCount-3); j++) {  
						numList[j + 2] = ns[j];
					}
				}
				for (i = pageIndex - infront; i <= pageIndex + inback; i++) {
					ns.push(i);
				}
				for (j = 0; j < (this.op.listCount-2); j++) {
					numList[j + 2] = ns[j];
				}
			} else {              
				if (this.pageCount >= this.op.listCount) {                               
					for (i = 0; i < this.op.listCount; i++) {
						numList[i] = i+1;
					}
				} else {                        
					for (i = 0; i < this.pageCount; i++) {
						numList[i] = i+1;
					}
				}
			}
			return numList;
		},
		//生成页码
		InitPager : function(pageIndex){
			$("#"+this.op.pagerName).html('');
			if(this.op.enableFirst==false&&this.pageCount<=1){
				return null;
			}
			var array = new Array();
			//var finalarr = new Array();
			var $con = $("#"+this.op.pagerName);
			//var pageIndex = parseFloat(pageIndex);
			switch(this.op.template){	//选择模板
				case 'default':array = this.InitDefaultList(pageIndex,this.pageCount);break;
				default:array = this.InitDefaultList(pageIndex,this.pageCount);
			}
			if(!array instanceof Array){
				throw new Error("is not array");
			} 
			if(array.length!=this.op.listCount){
				throw new Error("array.length error:"+array.length);
			}
			if(pageIndex>1&&this.op.enablePrevNext){
				$con.append(this.FormatStr(pageIndex-1,'上一页'));      
			}	
			for(var i=0;i<array.length;i++){
				if(typeof array[i]=='undefined'){
					continue;
				}
				if(pageIndex==array[i]){
					$con.append(this.FormatStrIndex(array[i]));
				}else if(typeof array[i]=='number'){
					$con.append(this.FormatStr(array[i],array[i]));
				}else{
					$con.append(array[i]);
				}
			}
			if(pageIndex<this.pageCount&&this.op.enablePrevNext){
				$con.append(this.FormatStr(pageIndex+1,'下一页')); 			
			}
			//$("#"+this.op.pagerName).append(finalarr);
		}
	}
	
    Plugin.prototype = {
		//初始化
        init: function() {
			var options = this.options;
            var $thisbase = $(this.element);
			var $content;
			if($thisbase.is(':has(tbody)')){					
				$content=$thisbase.children();
			}
			else{
				$content=$thisbase;
			}	
			var count = options.mode=='static'?$content.children().length:options.dataCount;		
			var eachcount = options.viewCount;				
			var totalpage = Math.ceil(count / eachcount); 
			var $pager = $("#"+options.pagerName);
			var setpager = new SetPager(options,totalpage);		//init
			if(options.mode=='url'){
				//修改获取当前页的方式,传入currentPage
				//var urlindex = getQueryString("p");
				var urlindex = options.currentPage;
				if(isNaN(urlindex)){
					setpager.InitPager(1);
				}else{
					urlindex = parseFloat(urlindex);
					setpager.InitPager(urlindex>totalpage?totalpage:urlindex);
				}
			}else{
				setpager.InitPager(1);
				if(options.mode=='static'&&typeof options.callback!='function'){
					Bind_StaticData($content,0,eachcount);
				}else{
					options.callback($content,1,options.viewCount);
				}
				$pager.bind("click",function(e){		//click事件
					if(e.target.tagName!='A') return;
					var $this = $(e.target);
					$this.removeAttr("href").siblings().attr("href", "javascript:void(0);");//..
					var indexnum = parseInt($this.html())==$this.html()?parseInt($this.html()):parseInt($this.attr('i'));
					var maxnum = (indexnum * eachcount);
					var minnum = (indexnum - 1) * eachcount;
					if(options.mode!='static'&&options.mode!='ajax'){
						throw new Error("mode must be selected:static,url,ajax");
					}
					if(options.mode=='static'&&typeof options.callback!='function'){
						setpager.InitPager(indexnum);
						Bind_StaticData($content,minnum, maxnum);
					}else{
						setpager.InitPager(indexnum);
						options.callback($content,indexnum,options.viewCount);
					}
				});
			}
        }
    };
	
	
    $.fn[pluginName] = function ( options ) {
        return this.each(function () {
            if (!$.data(this, "plugin_" + pluginName)) {
                $.data(this, "plugin_" + pluginName, new Plugin( this, options ));
            }
        });
    };

})( jQuery, window, document );