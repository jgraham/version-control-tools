/**
 * MRReviewFlag is responsible for showing the r?, r+, r- select dropdown
 * in the review dialog. It will also do the work of setting the extraData
 * in a Review model with the value that the user selects.
 */
MRReviewFlag = {};


MRReviewFlag.View = Backbone.View.extend({
  /**
   * If we save state, it'll be to a Review's extraData using this
   * key. This is the js counterpart of mozreview.extra_data.REVIEW_FLAG_KEY
   */
  key: 'p2rb.review_flag',

  /**
   * These are the possible states that will be shown in the dropdown,
   * in order. These are also the values that will be stored in the
   * extraData field.
   */
  states: [' ', 'r?', 'r+', 'r-'],

  template: _.template([
      '<label for="mr-review-flag" hidden>Review state:</label> ',
      '<select id="mr-review-flag">',
      '<% _(states).each(function(state) { %>',
      '  <option <% if (state === val) { %> selected <% } %> >',
      '    <%= state %>',
      '  </option>',
      '<% }); %>',
      '</select>'
  ].join('')),

  events: {
    'change #mr-review-flag': 'updateReviewState'
  },

  initialize: function() {
    _super(this).initialize.call(this);

    /**
    *  The first time a ReviewDialogHook is rendered, it will then retrieve
    *  the model data off the server and update the extraData. We have to
    *  wait for that update, and then re-render in order to show the value
    *  that is being stored server-side.
    */

    this.listenTo(this.model, 'change:extraData', _.bind(this.render, this));
  },

  /**
  *  Under some circumstances a model save will replace the comment textarea
  *  with a 'Add text' link. This is a hack to circumvent that problem.
  *  See bug 1273954.
  */
  save: function() {
    this.model.save({
      attrs: ['extra_data.' + this.key],
      success: function() {
        if (RB.ReviewDialogView._instance) {
          setTimeout(function() { RB.ReviewDialogView._instance._bodyTopView.openEditor(); }, 0);
        }
      }
    });
  },

  render: function() {
    var lastKnownFlag = ' ';
    var userReviewFlag = $('#user-review-flag');

    if (userReviewFlag.length == 1) {
      lastKnownFlag = $('#user-review-flag').data('reviewer-flag');
    }

    this.$el.html(this.template({
      states: this.states,
      val: this.model.get('extraData')[this.key] || lastKnownFlag
    }));

    return this;
  },

  updateReviewState: function() {
    var val = this.$el.find('#mr-review-flag').val();
    // We have to send the 'clear the flag' as a non empty string because
    // the api endpoint will ignore it otherwise.
    if (val === '') {
      val = ' ';
    }
    this.model.get('extraData')[this.key] = val;
    this.save();
  }
});


MRReviewFlag.Extension = RB.Extension.extend({
  initialize: function() {
    _super(this).initialize.call(this);
    $(document).on('mozreview_ready', _.bind(function() {
      if (!MozReview.isParent) {
        new RB.DraftDialogHook({
          extension: this,
          viewType: MRReviewFlag.View
        });
        $(document).trigger('mozreview_review_flag_ready');
      }
    }, this));
  }
});


RB.DraftDialogHook = RB.ExtensionHook.extend({
  hookPoint: new RB.ExtensionHookPoint(),

  defaults: _.defaults({
    viewType: null
  }, RB.ExtensionHook.prototype.defaults),

  setUpHook: function() {
    console.assert(this.get('viewType'),
                   'DraftDialogHook instance does not have a ' +
                   '"viewType" attribute set.');
  }
});
