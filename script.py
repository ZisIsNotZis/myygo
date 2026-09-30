'''
script: [effect...]
effect: [
	type,loc,
	condFn,
	costChkFn,costFn,
	opChkFn,opTargetFn,opFn,
	countLimit,flag
]
type: (active type) IGNITE,QUICK,ACTIVE...
	("be done" trigger type) SUMED,SPSUMED,DESTROYED,REMOVED,GRAVED,HANDED,ATKED,BATTLEDESTROYED...
	("do" trigger type) ATKING,BATTLEDESTROYING...
	(global trigger type) ANYSUMED,ANYSPSUMED,ANYDESTROYED,ANYREMOVED,ANYGRAVED,ANYHANDED,ANYATKED,ANYBATTLEDESTROY...
	(continuous type) EXACT,EXLEVEL,SETATK,NOATK,NOSUM_RETRIVELIMSPSUM,LIMSPSUM...
	((sp)summon proc type) SUM,SPSUM...
loc: None=auto
	=HAND for summon proc type
	=FIELD for IGNITE
	=ALL otherwise
fn: lambda with infered argument
	c=current card
	tp=current player
	eg="be done" cards
	ep="be done" player
	ev=related value
	re=reason effect
	r=reason (xor of EFFECT,BATTLE,COST,MATERIAL...)
	rp=reason player
	rg=reason cards
	tg=target cards (=c initially, =return value of parent function for chained functions)
condFn: Whether can use, return bool
costChkFn: Whether can cost, return boolable
costFn: Apply cost, return bool, tg is value returned by costChkFn
opChkFn: Whether can op, return boolable
opTargetFn: For op with target cards, select target for op, return targets, tg is value returned by opChkFn
opFn: Apply op, usually don't return, tg is value returned by opTargetFn if exist with non related cards removed, or value returned by calling opChkFn again
countLimit: either countPerTurn or [countPerTurn,sharedCounterId] where sharedCounterId<10 is private to same code cards, otherwise is shared across all cards
flag: xor of CONTINUOUS(force activate,no chain),FORCE,NODISABLE,NONEGATE,TOEQUIPER(give effect to equipper),TOOVERLAYER...

L: Partial helper. L.fn(*arg,**kwarg) => lambda x:x.fn(*arg,**kwarg). Supports boolean operation. L.f1(...)and L.f2(...) => lambda x:x.f1(...)and x.f2(...)
Cards: Class for card and cards, like string, where both no card, one card, or multi cards are always a Cards instance, and there's no Card (i.e. singlular form) class. Cards has truthity like list where empty is false. Cards.is/was/has/can... essentially filters.
Global functions:
	Get(filter:fn, selfZone:int, oppoZone=0) -> Cards
	HasLoc() -> bool #has usable loc
	CanDraw(n=1, p=tp) -> n
	Draw(n=1, p=tp) -> n
	Damage(n, p=tp) -> n
	Recover(n, p=tp) -> n
	Register(effect..., dur=inf) #register effect to player
Cards funcs:
	Cards.isUp()
	Cards.isSet(set:int)
	Cards.isCode(code:int)
	Cards.isRace(race:int)
	Cards.isAtr(atr:int)
	Cards.isType(type:int)
	Cards.isGtAtk(atk:int)
	...
	Cards.hasLoc() #has usable loc under this card
	...
	Cards.canSpsummon(pos=UP)
	Cards.canGrave()
	Cards.canRemove()
	Cards.canHand()
	...
	Cards.spsummon(pos=UP) #actually do this op
	Cards.grave()
	Cards.remove()
	Cards.hand()
	...
	Cards.register(effect...:Effect..., dur=inf) #register effect to card
'''
'''这个卡名的①②的效果1回合各能使用1次。
①：自己场上有「银河眼」怪兽存在的场合才能发动。这张卡从手卡守备表示特殊召唤。
②：超量素材的这张卡为让超量怪兽的效果发动而被取除的场合才能发动。从手卡·卡组选1只「银河眼光子龙」特殊召唤或在自己的超量怪兽下面重叠作为超量素材。这个效果在战斗阶段发动的场合，再让自己场上的全部「No.」超量怪兽的攻击力变成2倍。'''
[
	[
		IGNITE,HAND,
		lambda:Get(L.isUp()and L.isSet(0x107b),MZONE),
		None,None,
		lambda c:HasLoc()and c.canSpsum(DEF),None,lambda t:t.spsum(DEF),
		[1,0],
	],
	[
		DETACHED,None,
		None,
		None,None,
		lambda:Get(Get(L.isType(XYZ),MZONE)or(HasLoc()and L.canSpsum())and L.isCode(93717133),HAND+DECK),None,lambda tg:Choose(
			spsum=[(c:=tg.select()).canSpsum(),lambda:c.spsum()],
			overlay=Get(L.isType(XYZ),MZONE),lambda tg:c.overlay(tg.select())
		)
		[1,1],
	],
]
'''①：这张卡可以把自己场上2只攻击力2000以上的怪兽解放从手卡特殊召唤。
②：这张卡和对方怪兽进行战斗的战斗步骤，以那1只对方怪兽为对象才能发动。那只对方怪兽和场上的这张卡除外。这个效果除外的怪兽在战斗阶段结束时回到场上，这个效果把超量怪兽除外的场合，这张卡的攻击力上升把那只超量怪兽除外时的超量素材数量×500。'''
[
	[
		SPSUM,None,
		None,
		lambda:Get(HasLoc()or L.canLoc() and L.isGeAtk(2000),MZONE).min(2),lambda tg:tg.select(2).release()
	],
	[
		[ATKING,ATKED],None,
		None,
		None,None,
		lambda c,eg,rg:eg.canRemove()and rg.canRemove()and(rg if c==atk else atk).canTarget(),L.identity(),lambda c,tg:[
			n:=tg.countAttach(),
			c.isRelate().add(tg).remove().delay(BATTLED,lambda tg:tg.ret().isIn(c).exAtk(n*500))
		]
	]
]
'''这个卡名的①的方法的特殊召唤1回合只能有1次，②③的效果1回合各能使用1次。
①：自己场上有「王之棺」存在的场合，这张卡可以从墓地特殊召唤。
②：把包含这张卡的2张手卡送去墓地才能发动。从卡组把1张「王之棺」加入手卡。那之后，自己可以抽1张。
③：这张卡在怪兽区域存在的状态，自己场上的其他卡因对方的效果从场上离开的场合才能发动。场上1张卡送去墓地。'''
[
	[
		SPSUM,GRAVE,
		lambda:Get(L.isCode(16528181)and L.isUp(),SZONE),
		None,None,
		None,None,None,
		[1,0],
	],
	[
		IGNITE,HAND,
		None,
		lambda c:c.canGrave()and Get(L.canGrave(),HAND),lambda c,tg:c.grave()and tg.select().grave(),
		lambda:Get(L.isCode(16528181)and L.canHand(),DECK),None,lambda tg:tg.select().hand()
		[1,1],
	],
	[
		ANYLEAVED,MZONE,
		lambda tp,eg,r,rp:eg.wasController(tp)and r|EFFECT and rp!=tp
		None,None,
		None,None,lambda:Select(True,FIELD).grave()
		[1,2],
	]
]
'''①：自己场上有「光子」怪兽或者「银河」怪兽存在的场合，这张卡可以不用解放作召唤。
②：这张卡的①的方法召唤成功的场合，以自己墓地1只「银河眼光子龙」为对象发动。这张卡的攻击力直到回合结束时下降1000，作为对象的怪兽守备表示特殊召唤。'''
[
	e:=[
		SUM,None,
		lambda:Get(L.isSet(0x55,0x7b),MZONE),
	],
	[
		SUMED,None,
		lambda re:re==e,
		None,None,
		lambda:HasLoc()and Get(L.isCode(93717133)and L.canSpsum(DEF)and L.canTarget(),GRAVE),L.select(),lambda c,t:c.exAtk(-1000,1)and t.spsum(DEF)
	]
]
'''这个卡名的①的效果1回合只能使用1次。
①：这张卡从场上以外送去墓地的场合，若这张卡以外的「光子」怪兽或「银河」怪兽在自己的场上或墓地存在则能发动。这张卡守备表示特殊召唤。
②：这张卡召唤·特殊召唤时适用。这个回合，自己在通常召唤外加上只有1次，自己主要阶段可以把1只光属性怪兽召唤。
'''
[
	[
		GRAVED,None,
		lambda c:Get(L.isSet(0x55,0x7b)and not L.isIn(c),MZONE+GRAVE),
		None,None,
		lambda c:HasLoc()and c.canSpsum(DEF),None,L.spsum(DEF)
	],
	[
		SPSUM,None,
		None,None,
		None,None,None,
		lambda:Register([
			EXSUM,
			None,
			None,
			None,None,
			lambda c,tp:c.isAtr(LIGHT)and c.isController(tp)
		],1),
		None,CONTINUOUS,
	]
]
'''这个卡名的①的方法的特殊召唤1回合只能有1次，②的效果1回合只能使用1次。
①：自己场上有「王之棺」存在的场合，这张卡可以从墓地特殊召唤。
②：这张卡在怪兽区域存在的状态，自己场上的其他卡因对方的效果从场上离开的场合，从双方的墓地·除外状态的卡之中以合计2张为对象才能发动。那2张卡加入持有者手卡或那2张卡回到卡组。'''
[
	[
		SPSUM,GRAVE,
		lambda:Get(L.isCode(16528181)and L.isUp(),SZONE),
		None,None,
		None,None,None,
		[1,0],
	],
	[
		ANYLEAVED,MZONE,
		lambda tp,eg,r,rp:eg.wasController(tp)and r|EFFECT and rp!=tp
		None,None,
		lambda:Get(None,GRAVE+REMOVE,GRAVE+REMOVE).min(2),L.select(2),lambda tg:Choose(
			hand=[tg.canHand(),L.hand()],
			deck=[True,L.deck()],
		),
		[1,2],
	]
]
'''①：自己场上有「王之棺」存在的场合，这张卡可以从墓地特殊召唤。
②：这张卡的攻击力·守备力上升自己场上的「荷鲁斯」怪兽数量×1200。
③：这张卡在怪兽区域存在的状态，自己场上的其他卡因对方的效果从场上离开的场合才能发动。自己抽出自己的主要怪兽区域的怪兽种类的数量。'''
[
	[
		SPSUM,GRAVE,
		lambda:Get(L.isCode(16528181)and L.isUp(),SZONE),
		None,None,
		None,None,None,
		[1,0],
	],
	[
		EXATK,None,
		None,
		None,None,
		None,None,lambda:Count(L.isSet(0x19d)and L.isUp())*1000,
	],
	[
		ANYLEAVED,MZONE,
		lambda tp,eg,r,rp:eg.wasController(tp)and r|EFFECT and rp!=tp
		None,None,
		lambda:CanDraw(Get(None,MZONE).count(L.getCode())),None,lambda tg:Draw(tg),
		[1,2],
	],
]
'''这个卡名的②的效果1回合只能使用1次。
①：从手卡把1只其他的光属性怪兽送去墓地才能发动。这张卡从手卡守备表示特殊召唤。
②：这张卡特殊召唤时才能发动。从卡组把1只「银河」怪兽加入手卡。'''
[
	[
		IGNITE,HAND,
		None,
		lambda c:Get(L.isAtr(LIGHT)and L.canGrave()and not L.isIn(c),HAND),lambda tg:tg.select().grave(),
		lambda c:HasLoc()and c.canSpsum(DEF),None,L.spsum(DEF),
	],
	[
		SPSUMED,None,
		None,
		None,None,
		lambda:Get(L.isSet(0x7b)and L.isMon() and L.canHand(),DECK),None,lambda tg:tg.select().hand()
	]
]
'''这张卡不能通常召唤。自己场上有「光子」怪兽或「银河」怪兽存在的场合可以特殊召唤。自己对「光子驱逐者」1回合只能有1次特殊召唤。
①：这张卡特殊召唤的场合才能发动。从卡组把1只「银河眼光子龙」加入手卡。
②：这张卡在特殊召唤的回合不能攻击。
③：场上的这张卡为素材作超量召唤的怪兽得到以下效果。
●这张卡战斗破坏的怪兽不去墓地而除外。'''
[
	[
		NOSUM_RETRIVELIMSPSUM,None,
		lambda:Get(L.isSet(0x55,0x7b)and L.isUp,MZONE),
	],
	[
		LIMSPSUM,None,
		None,
		None,None,
		None,None,None,
		[1,0],
	],
	[
		SPSUMED,None,
		None,
		None,None,
		lambda:Get(L.isSet(93717133)and L.canHand(),DECK),None,lambda tg:tg.any().hand(),
	],
	[
		NOATK,None,
		lambda c:GetTurn()==c.getTurn(),
	],
	[
		XYZMATED,None,
		None,
		None,None,
		None,None,lambda rg:rg.register([
			BATTLEDESTROYING,None,
			None,
			None,None,
			None,None,lambda eg:eg.remove(),
		]),
		None,CONTINUOUS,
	],
]
'''这个卡名的①②的效果1回合各能使用1次。
①：这张卡召唤·特殊召唤的场合，以「银河召唤师」以外的自己墓地1只「光子」怪兽或「银河」怪兽为对象才能发动。那只怪兽守备表示特殊召唤。
②：以自己场上1只其他的光属性怪兽为对象才能发动。那只怪兽的等级直到回合结束时变成4星。'''
[
	[
		[SUMED,SPSUMED],None,
		None,
		None,None,
		lambda:HasLoc()and Get(L.isSet(0x55,0x7b)and not L.isCode(863795)and L.canSpsum(DEF)and L.canTarget(),GRAVE),
		L.select(),
		L.spsum(DEF),
		[1,0],
	],
	[
		IGNITE,None,
		None,None,
		None,lambda c:Get(L.isUp() and L.isAtr(LIGHT)and not L.isLevel(4)and L.canTarget()and not L.isIn(c),MZONE),L.select(),
		L.setLevel(4,1),
	]
]
'''这个卡名的②的效果1回合只能使用1次。
①：以自己场上1只「光子」怪兽或「银河」怪兽为对象才能发动。从自己的手卡·场上把这张卡当作持有以下效果的装备魔法卡使用给那只自己怪兽装备。
●装备怪兽的攻击力上升500，不会被战斗破坏。
②：把装备的这张卡送去墓地才能发动。除「光子轨道」外的1只「光子」怪兽或「银河」怪兽从卡组加入手卡。'''
[
	[
		IGNITE,HAND+MZONE,
		None,
		None,None,
		lambda c:HasLoc(SZONE)and Get(L.isUp() and L.isSet(0x55,0x7b)and L.canTarget()and not L.isIn(c),MZONE),L.select(),lambda c,tg:tg.equip(c.isRelate()).register([
			EXATK,None,
			None,None,
			None,None,lambda:500,
			None,TOEQUIPER,
		],[
			NOBATTLEDESTROY,None,
			None,None,
			None,None,None,
			None,TOEQUIPER,
		])
	],
	[
		IGNITE,EQUIP,
		None,
		None,None,
		lambda:Get(L.isSet(0x55,0x7b)and L.canHand(),DECK),None,lambda tg:tg.select().hand()
	]
]
'''①：1回合1次，自己主要阶段才能发动。这张卡的等级直到回合结束时上升4星。
②：把这张卡解放才能发动。从卡组把「银河魔导师」以外的1张「银河」卡加入手卡。'''
[
	[
		IGNITE,None,
		None,
		None,None,
		None,None,lambda c:c.isRelate().exLevel(4,1),
		1
	],
	[
		IGNITE,None,
		None,
		L.canRelease(),L.release(),
		lambda:Get(L.isSet(0x7b)and not L.isCode(98555327)and L.canHand(),DECK),None,lambda tg:tg.select().hand()
	]
]

