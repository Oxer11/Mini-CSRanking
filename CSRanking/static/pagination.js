(function () {
  /*global Modernizr:true */
  'use strict';
  (function ($) {
    $.fn.extend({
      mgPgnation: function (options) {
        /* func :: calculate width of each page num */
        /* func :: draw magic line */
        /* func :: update prev text */
        var $curNav, $magicLine, $magicNav, $mainNav, $nextNav, $pgnNav, $prevNav, $prevNavText, $this, calPgnWidth, magicDraw, prevNavWidth, prevText, showPrevNext, updatePrevText;
        $this = $(this);
        if ($this.length) {
          $mainNav = this.children();
          $pgnNav = $this.find('.pgn__item');
          $curNav = $this.find('.current');
          $magicNav = $this.find('a');
          $prevNav = $this.find('.prev');
          $nextNav = $this.find('.next');
          $prevNavText = $prevNav.find('.pgn__prev-txt');
          updatePrevText = function () {
            $prevNavText = $prevNav.find('.pgn__prev-txt');
            return $prevNavText.html('Prev');
          };
          calPgnWidth = function () {
            var pgnWidth, prevWidth, vsbNav, vsbNavs;
            // number of visible <a> plus <strong class="current">
            vsbNav = $this.find('.pgn__item a:visible').length + 1;
            vsbNavs = vsbNav + 2;
            prevWidth = 100 / vsbNavs;
            pgnWidth = 100 - prevWidth * 2;
            $prevNav.css('width', prevWidth + '%');
            $nextNav.css('width', prevWidth + '%');
            $pgnNav.css('width', pgnWidth + '%');
            // <a> and <strong>
            return $pgnNav.find('a, strong').css('width', 100 / vsbNav + '%');
          };
          /* func :: calculate and display prev/next */
          // 85px - display full text
          showPrevNext = function () {
            var prevNavWidth;
            prevNavWidth = $prevNav.innerWidth();
            if (prevNavWidth > 100) {
              $this.addClass('fullprevnext');
              // display Previous
              return $prevNavText.html('Previous');
            } else if (prevNavWidth < 101 && prevNavWidth > 60) {
              $this.addClass('fullprevnext');
              // display Prev
              return $prevNavText.html('Prev');
            } else {
              return $this.removeClass('fullprevnext');
            }
          };
          magicDraw = function () {
            // draw init magic line
            $magicLine.width($curNav.width());
            if ($curNav.position() !== void 0) {
              $magicLine.css('left', $curNav.position().left);
            }

            // assign orig values
            $magicLine.data('origLeft', $magicLine.position().left);
            return $magicLine.data('origWidth', $magicLine.width());
          };
          // END funcs

          // create magic line
          $mainNav.append('<li class="pgn__magic-line">');

          // declare magic line
          $magicLine = $this.find('.pgn__magic-line');
          // add extra class & element if no prev or next
          prevNavWidth = $prevNav.innerWidth();
          if (prevNavWidth > 100) {
            prevText = 'Previous';
          } else {
            prevText = 'Prev';
          }
          if (!$prevNav.children().length) {
            $prevNav.addClass('disabled');
            $prevNav.append('<a rel="prev"><i class="pgn__prev-icon icon-angle-left"></i><span class="pgn__prev-txt">' + prevText + '</span></a>');
          }
          if (!$nextNav.children().length) {
            $nextNav.addClass('disabled');
            $nextNav.append('<a rel="next"><i class="pgn__next-icon icon-angle-right"></i><span class="pgn__next-txt">Next</span></a>');
          }
          // calculate pgn width
          calPgnWidth();
          // show prev/next
          showPrevNext();
          // draw magic line
          magicDraw();

          // when hover
          $magicNav.hover(function () {
            var $el, leftPos, newWidth;
            $el = $(this);
            leftPos = $el.position().left;
            newWidth = $el.width();

            // animate magic line
            return $magicLine.stop().animate({
              left: leftPos,
              width: newWidth });

          }, function () {
            return $magicLine.stop().animate({
              left: $magicLine.data('origLeft'),
              width: $magicLine.data('origWidth') });

          });
          /* Window Resize Changes */
          return window.addEventListener('resize', function () {
            updatePrevText();
            calPgnWidth();
            showPrevNext();
            return magicDraw();
          });
        }
      } });

    // END mgPgnation()

    // call function here
    return $('.pgn').mgPgnation();
  })(jQuery);

}).call(this);

//# sourceURL=coffeescript