import { CheckCircle2, AlertTriangle } from 'lucide-react';
import { Alternative } from '@/lib/types';
import { money } from '@/lib/api';
export default function OptionCard({option, selected, suggested, disabled, onSelect}:{option:Alternative;selected:boolean;suggested:boolean;disabled:boolean;onSelect:()=>void}) {
  return <button type="button" className={`option ${selected?'selected':''}`} onClick={onSelect} disabled={disabled} aria-pressed={selected} aria-label={`Select ${option.supplier_name}`}>
    <div className="flex-between"><span className="eyebrow">{suggested?'BEST DELIVERY FIT':'LOWER QUOTED COST'}</span><span className="radio-dot">{selected?'●':'○'}</span></div>
    <h3>{option.supplier_name}</h3><p className="muted">Established supplier · synthetic quotation</p>
    <div className="option-price">{money(option.total_sen)}<span>total quotation</span></div>
    <div className="option-facts"><div><span>Price / litre</span><strong>{money(option.unit_price_sen)}</strong></div><div><span>Estimated delivery</span><strong>{option.lead_days} day{option.lead_days!==1?'s':''}</strong></div><div><span>Premium vs cheapest</span><strong>{money(option.premium_sen)}</strong></div><div><span>Coverage after arrival</span><strong>{option.coverage_after_arrival_days} days*</strong></div></div>
    <div className={`risk-note ${option.stockout_risk?'risk':'safe'}`}>{option.stockout_risk?<AlertTriangle size={17}/>:<CheckCircle2 size={17}/>}<span>{option.risk}</span></div>
  </button>;
}
