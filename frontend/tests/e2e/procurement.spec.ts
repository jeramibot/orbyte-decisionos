import {test,expect} from '@playwright/test';
test('shortage → comparison → owner approval → persistent PO and audit',async({page})=>{
 await page.goto('/');
 await expect(page.getByRole('heading',{name:'Your business, in focus.'})).toBeVisible();
 await page.getByRole('button',{name:'Run inventory check'}).click();
 await expect(page.getByRole('heading',{name:'Fresh milk replenishment'})).toBeVisible();
 await expect(page.getByText('RM570.00')).toBeVisible();
 await expect(page.getByText('RM660.00')).toBeVisible();
 await expect(page.getByText('RM90.00')).toBeVisible();
 await expect(page.getByText('Delivery exceeds stock coverage by 2.5 days')).toBeVisible();
 await expect(page.getByRole('button',{name:'Approve & create draft'})).toBeDisabled();
 await page.getByLabel('Demo role').selectOption('owner-demo');
 const b=page.getByRole('button',{name:'Select Supplier B · Metro Fresh'});
 await expect(b).toBeEnabled(); await b.click();
 await page.getByLabel('Reason for this decision').fill('Pay RM90 more for estimated delivery before stock runs out.');
 await page.getByRole('button',{name:'Approve & create draft'}).click();
 await expect(page.getByRole('heading',{name:'Purchase-order draft ready'})).toBeVisible();
 await expect(page.getByText('purchase order draft created',{exact:true})).toBeVisible();
 const url=page.url();await page.reload();
 await expect(page.getByRole('heading',{name:'Purchase-order draft ready'})).toBeVisible();
 await expect(page.getByRole('button',{name:'Approve & create draft'})).toHaveCount(0);
 expect(page.url()).toBe(url);
 await page.getByRole('link',{name:'Audit log',exact:true}).click();
 await expect(page.getByText('purchase order draft created',{exact:true})).toBeVisible();
});
test('owner rejection creates no order',async({page})=>{
 await page.goto('/operations');await page.getByLabel('Demo role').selectOption('owner-demo');
 await page.getByRole('button',{name:'Check milk stock'}).click();
 await page.getByLabel('Reason for this decision').fill('Check storage capacity before buying.');
 await page.getByRole('button',{name:'Reject request'}).click();
 await expect(page.getByText('rejected',{exact:true}).first()).toBeVisible();
 await expect(page.getByRole('heading',{name:'Purchase-order draft ready'})).toHaveCount(0);
});
test('simulation unavailable is explicit and has no generated report',async({page})=>{
 await page.goto('/simulations');await page.getByLabel('Demo role').selectOption('owner-demo');
 await page.getByRole('button',{name:'Check simulation availability'}).click();
 await expect(page.getByText('No completed simulation report. No insights have been generated.')).toBeVisible();
 await expect(page.getByText('Tokens: Not reported',{exact:false})).toBeVisible();
});
test('mobile navigation and content stay within viewport',async({page})=>{
 await page.setViewportSize({width:390,height:844});await page.goto('/');
 await expect(page.getByRole('heading',{name:'Your business, in focus.'})).toBeVisible();
 await page.getByRole('button',{name:'Open navigation'}).click();await page.getByRole('link',{name:'Operations',exact:true}).click();
 await expect(page.getByRole('heading',{name:'Keep the essentials flowing.'})).toBeVisible();
 expect(await page.evaluate(()=>document.documentElement.scrollWidth<=window.innerWidth)).toBe(true);
});
