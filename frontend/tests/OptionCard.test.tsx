import { render, screen, fireEvent } from '@testing-library/react';
import { describe,it,expect,vi } from 'vitest';
import OptionCard from '../components/OptionCard';
const option={id:'offer-b',supplier_id:'b',item_id:'milk',version:1,supplier_name:'Supplier B',unit_price_sen:1100,lead_days:1,total_sen:66000,premium_sen:9000,stockout_risk:false,stockout_gap_days:0,coverage_after_arrival_days:5.5,risk:'Within estimated stock coverage'};
describe('Supplier comparison',()=>{
 it('shows verified currency values and invokes deliberate selection',()=>{const select=vi.fn();render(<OptionCard option={option} selected={false} suggested disabled={false} onSelect={select}/>);expect(screen.getByText('RM660.00')).toBeInTheDocument();expect(screen.getByText('RM90.00')).toBeInTheDocument();fireEvent.click(screen.getByRole('button',{name:'Select Supplier B'}));expect(select).toHaveBeenCalledOnce();});
 it('blocks selection when the role cannot approve',()=>{const select=vi.fn();render(<OptionCard option={option} selected={false} suggested disabled onSelect={select}/>);const button=screen.getByRole('button');expect(button).toBeDisabled();fireEvent.click(button);expect(select).not.toHaveBeenCalled();});
 it('surfaces stockout warning and selection state',()=>{render(<OptionCard option={{...option,stockout_risk:true,risk:'Delivery exceeds coverage by 2.5 days'}} selected suggested={false} disabled={false} onSelect={()=>{}}/>);expect(screen.getByText('Delivery exceeds coverage by 2.5 days')).toBeInTheDocument();expect(screen.getByRole('button')).toHaveAttribute('aria-pressed','true');});
});
