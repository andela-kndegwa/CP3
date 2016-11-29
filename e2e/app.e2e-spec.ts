import { CP3Page } from './app.po';

describe('cp3 App', function() {
  let page: CP3Page;

  beforeEach(() => {
    page = new CP3Page();
  });

  it('should display message saying app works', () => {
    page.navigateTo();
    expect(page.getParagraphText()).toEqual('app works!');
  });
});
