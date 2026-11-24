# ФРОНТЛАЙН: ПЕПЕЛ — командный шутер для Roblox (в духе The Lost Front)

Всё оригинальное: названия, оружие, меню, карта и костюмы придуманы с нуля и **не копируют** чужие ассеты.
Карта и оружие строятся кодом из стандартных материалов Roblox (бетон, кирпич, ржавый металл), так что вам не нужно ничего импортировать.

---

## ЧАСТЬ 1. Подготовка в Roblox Studio

1. Откройте **Roblox Studio → New → Baseplate**.
2. В Explorer **удалите `Baseplate` и `SpawnLocation`** (карту создаст скрипт).
3. **Home → Game Settings → Avatar → Avatar Type = R15**.
4. **Game Settings → Security → включите "Enable Studio Access to API Services"** (нужно для сохранения данных).
5. Создайте объекты строго с этими именами и типами:

| № | Где | Тип | Имя | Код из |
|---|-----|-----|-----|--------|
| 1 | ReplicatedStorage | **ModuleScript** | `Config` | Часть 2 |
| 2 | ServerScriptService | **Script** | `MapBuilder` | Часть 4 |
| 3 | ServerScriptService | **Script** | `Main` | Часть 3 |
| 4 | StarterPlayer → StarterPlayerScripts | **ModuleScript** | `ClientState` | Часть 5 |
| 5 | StarterPlayer → StarterPlayerScripts | **LocalScript** | `GameClient` | Часть 6 |
| 6 | StarterPlayer → StarterPlayerScripts | **LocalScript** | `MenuClient` | Часть 7 |

Как создать: правый клик по контейнеру → **Insert Object** → нужный тип → **F2** для переименования → двойной клик и вставьте код целиком (сначала удалите стандартную строку `print("Hello world!")`).

6. Монетизация (позже, в Creator Dashboard → ваш плейс → **Monetization**):
   - создайте **Game Pass** «VIP» → скопируйте ID в `Config.VIPGamePassId`;
   - создайте **3 Developer Products** для кредитов и **3 Developer Products** для «Поддержать меня» → вставьте их ID в `Config.Products`.
   - Цены в `Robux = ...` в Config нужны только для подписи на кнопках, реальная цена берётся из настроек продукта. Пока ID = 0, кнопки покупки просто покажут сообщение.
7. Нажмите **Play** для теста. Для мобильного режима: **Test → Device** (эмулятор телефона).

---

## ЧАСТЬ 2. `Config` (ModuleScript в ReplicatedStorage)

```lua
local Config = {}

Config.GameName = "ФРОНТЛАЙН: ПЕПЕЛ"
Config.ScoreToWin = 50          -- убийств для победы команды
Config.RespawnTime = 4

------------------------------------------------------------
-- МОНЕТИЗАЦИЯ: вставьте свои ID (0 = пока не настроено)
------------------------------------------------------------
Config.VIPGamePassId = 0
Config.Products = {
	Credits = {   -- донат валюты (кредиты)
		{Id = 0, Amount = 500,  Robux = 49},
		{Id = 0, Amount = 1500, Robux = 129},
		{Id = 0, Amount = 5000, Robux = 399},
	},
	Support = {   -- "Поддержать меня"
		{Id = 0, Robux = 25},
		{Id = 0, Robux = 100},
		{Id = 0, Robux = 500},
	},
}

------------------------------------------------------------
-- КОМАНДЫ (две, как в оригинале)
------------------------------------------------------------
Config.Teams = {
	{Name = "Альфа", Color = BrickColor.new("Bright blue"), DefaultOutfit = 1},
	{Name = "Браво", Color = BrickColor.new("Bright red"),  DefaultOutfit = 3},
}

------------------------------------------------------------
-- КОСТЮМЫ (подбираются в ящиках на карте)
------------------------------------------------------------
Config.Outfits = {
	{Name = "Лесной камуфляж", Shirt = Color3.fromRGB(78,98,62),   Pants = Color3.fromRGB(62,76,52),   Helmet = Color3.fromRGB(60,72,50)},
	{Name = "Пустыня",         Shirt = Color3.fromRGB(176,150,104),Pants = Color3.fromRGB(150,128,90), Helmet = Color3.fromRGB(140,120,85)},
	{Name = "Городской серый", Shirt = Color3.fromRGB(96,100,106), Pants = Color3.fromRGB(70,74,80),   Helmet = Color3.fromRGB(50,54,60)},
	{Name = "Арктика",         Shirt = Color3.fromRGB(205,210,215),Pants = Color3.fromRGB(180,186,192),Helmet = Color3.fromRGB(160,166,172)},
	{Name = "Ночной рейд",     Shirt = Color3.fromRGB(32,36,44),   Pants = Color3.fromRGB(24,26,32),   Helmet = Color3.fromRGB(20,22,26)},
}

------------------------------------------------------------
-- СПОСОБНОСТИ (клавиша 3) И РОЛИ
------------------------------------------------------------
Config.Abilities = {
	Frag  = {Title = "Граната",   Cooldown = 15},
	Heal  = {Title = "Аптечка",   Cooldown = 25},
	Smoke = {Title = "Дым",       Cooldown = 30},
	FPV   = {Title = "FPV-дрон",  Cooldown = 45},
}

Config.RoleOrder = {"Assault", "Medic", "Sniper", "Drone"}
Config.Roles = {
	Assault = {Title = "Штурмовик",    Desc = "Крепкий боец первой линии. Метает осколочные гранаты.", Health = 110, Speed = 16, Ability = "Frag"},
	Medic   = {Title = "Медик",        Desc = "Лечит себя в бою и долго держится на ногах.",           Health = 100, Speed = 16, Ability = "Heal"},
	Sniper  = {Title = "Снайпер",      Desc = "Быстрый, но хрупкий. Ставит дымовую завесу.",           Health = 90,  Speed = 17, Ability = "Smoke"},
	Drone   = {Title = "Дронщик",      Desc = "Управляет FPV-дроном-камикадзе (клавиша 3 ещё раз — подрыв).", Health = 90, Speed = 15, Ability = "FPV"},
}

------------------------------------------------------------
-- ОРУЖИЕ (оригинальные названия, не копии чужих)
-- Slot 1 = основное, Slot 2 = запасное
-- Zoom = список уровней приближения (клавиша Z переключает по кругу)
------------------------------------------------------------
Config.Weapons = {
	-- ОСНОВНОЕ
	["Рейд-47"]    = {Slot=1, Type="Штурмовая винтовка", Damage=26, Head=1.8, RPM=600, Mag=30, Reserve=120, Range=300, Spread=1.0, Pellets=1, Auto=true,  Reload=2.3, Zoom={1.5},   Recoil=0.9, Price=0,    Color=Color3.fromRGB(50,50,52),   Size=Vector3.new(0.35,0.55,3.2)},
	["Карабин М-4"]= {Slot=1, Type="Штурмовая винтовка", Damage=22, Head=1.8, RPM=750, Mag=30, Reserve=150, Range=300, Spread=0.8, Pellets=1, Auto=true,  Reload=2.0, Zoom={1.5},   Recoil=0.7, Price=900,  Color=Color3.fromRGB(70,72,64),   Size=Vector3.new(0.35,0.55,3.0)},
	["Тихий-9"]    = {Slot=1, Type="Пистолет-пулемёт",  Damage=16, Head=1.6, RPM=900, Mag=32, Reserve=160, Range=200, Spread=1.6, Pellets=1, Auto=true,  Reload=1.8, Zoom={1.3},   Recoil=0.5, Price=700,  Color=Color3.fromRGB(40,40,44),   Size=Vector3.new(0.3,0.5,2.2)},
	["Дозор-12"]   = {Slot=1, Type="Дробовик",          Damage=11, Head=1.5, RPM=70,  Mag=6,  Reserve=36,  Range=90,  Spread=5.0, Pellets=8, Auto=false, Reload=3.0, Zoom={1.2},   Recoil=3.0, Price=1100, Color=Color3.fromRGB(90,62,40),   Size=Vector3.new(0.4,0.5,3.4)},
	["Сокол-М"]    = {Slot=1, Type="Снайперская винтовка", Damage=95, Head=2.2, RPM=45, Mag=5, Reserve=25, Range=800, Spread=0.05,Pellets=1, Auto=false, Reload=3.2, Zoom={4,8},     Recoil=4.0, Price=1800, Color=Color3.fromRGB(36,48,40),   Size=Vector3.new(0.3,0.5,4.2)},
	["Бастион-L"]  = {Slot=1, Type="Пулемёт",           Damage=24, Head=1.6, RPM=650, Mag=75, Reserve=225, Range=300, Spread=1.8, Pellets=1, Auto=true,  Reload=5.0, Zoom={1.4},   Recoil=1.0, Price=1500, Color=Color3.fromRGB(56,56,50),   Size=Vector3.new(0.4,0.6,3.6)},
	["Фантом-VIP"] = {Slot=1, Type="VIP-винтовка",      Damage=28, Head=2.0, RPM=650, Mag=30, Reserve=150, Range=320, Spread=0.7, Pellets=1, Auto=true,  Reload=2.0, Zoom={1.6},   Recoil=0.7, Price=0, VIPOnly=true, Color=Color3.fromRGB(212,175,55), Size=Vector3.new(0.35,0.55,3.2)},
	-- ЗАПАСНОЕ
	["Р-17"]       = {Slot=2, Type="Пистолет",          Damage=20, Head=2.0, RPM=400, Mag=15, Reserve=75,  Range=150, Spread=0.9, Pellets=1, Auto=false, Reload=1.6, Zoom={1.3},   Recoil=1.2, Price=0,    Color=Color3.fromRGB(45,45,48),   Size=Vector3.new(0.25,0.45,1.1)},
	["Кобра-50"]   = {Slot=2, Type="Тяжёлый револьвер", Damage=52, Head=2.0, RPM=120, Mag=7,  Reserve=35,  Range=200, Spread=0.6, Pellets=1, Auto=false, Reload=2.4, Zoom={1.3},   Recoil=3.0, Price=1200, Color=Color3.fromRGB(150,150,155),Size=Vector3.new(0.28,0.5,1.4)},
	["Колибри"]    = {Slot=2, Type="Автоматический пистолет", Damage=13, Head=1.5, RPM=800, Mag=20, Reserve=100, Range=120, Spread=2.0, Pellets=1, Auto=true, Reload=1.7, Zoom={1.2}, Recoil=0.8, Price=600, Color=Color3.fromRGB(35,35,38), Size=Vector3.new(0.25,0.45,1.2)},
}

------------------------------------------------------------
-- ЕЖЕНЕДЕЛЬНЫЕ АКЦИИ (меняются сами каждую неделю)
-- Discounts = скидка на оружие (0.4 = -40%), CreditMult = множитель кредитов за убийства
------------------------------------------------------------
Config.WeeklyDeals = {
	{Title = "Неделя снайпера",   Discounts = {["Сокол-М"] = 0.4}, CreditMult = 1},
	{Title = "Двойные кредиты",   Discounts = {},                  CreditMult = 2},
	{Title = "Распродажа SMG",    Discounts = {["Тихий-9"] = 0.5, ["Кобра-50"] = 0.3}, CreditMult = 1.5},
	{Title = "Неделя дронов",     Discounts = {["Колибри"] = 0.3}, CreditMult = 1.5, FPVCooldown = 0.5},
}
function Config.GetWeeklyDeal()
	local week = math.floor(os.time() / 604800)
	local deal = Config.WeeklyDeals[week % #Config.WeeklyDeals + 1]
	return deal, (week + 1) * 604800 - os.time()
end

------------------------------------------------------------
-- КЛАВИШИ И НАСТРОЙКИ ПО УМОЛЧАНИЮ
-- (Fire = ЛКМ, Crouch = C, 1/2 = оружие, 3 = способность, Z = зум)
------------------------------------------------------------
Config.DefaultKeys = {
	Fire = "MouseButton1", Crouch = "C", Slot1 = "One", Slot2 = "Two",
	Ability = "Three", Zoom = "Z", Reload = "R", Menu = "M",
}
Config.DefaultSettings = {
	FOV = 80, CrosshairColor = {80, 255, 80}, CrosshairSize = 10,
	Hitmarker = true, FirstPerson = true,
	MobileScale = 1, MobileOpacity = 0.6, MobilePos = {},
}

-- Звуки: вставьте свои rbxassetid://... из Toolbox (Audio). Пустая строка = без звука.
Config.Sounds = {Shot = "", Hit = "", Kill = ""}

return Config
```

---

## ЧАСТЬ 3. `Main` (Script в ServerScriptService)

```lua
local Players = game:GetService("Players")
local RS = game:GetService("ReplicatedStorage")
local Teams = game:GetService("Teams")
local DSS = game:GetService("DataStoreService")
local MPS = game:GetService("MarketplaceService")
local CS = game:GetService("CollectionService")
local Debris = game:GetService("Debris")
local Config = require(RS:WaitForChild("Config"))

Players.CharacterAutoLoads = false

local effects = workspace:FindFirstChild("Effects") or Instance.new("Folder")
effects.Name = "Effects"; effects.Parent = workspace

local store = DSS:GetDataStore("FrontlineAsh_v1")

------------------------------------------------------------ REMOTES
local Remotes = Instance.new("Folder"); Remotes.Name = "Remotes"; Remotes.Parent = RS
local function remote(name, class)
	local r = Instance.new(class or "RemoteEvent"); r.Name = name; r.Parent = Remotes; return r
end
local R = {}
for _, n in ipairs({"Fire","Reload","Equip","Ability","Deploy","SetRole","SetLoadout","SaveSettings",
	"KillFeed","HitMark","Damaged","Tracer","Notify","DroneStart","DroneEnd","DroneDetonate"}) do
	R[n] = remote(n)
end
R.Buy = remote("Buy", "RemoteFunction")
R.GetData = remote("GetData", "RemoteFunction")

------------------------------------------------------------ КОМАНДЫ
local teamObjs = {}
for _, t in ipairs(Config.Teams) do
	local team = Instance.new("Team")
	team.Name = t.Name; team.TeamColor = t.Color; team.AutoAssignable = false
	team:SetAttribute("Score", 0)
	team.Parent = Teams
	table.insert(teamObjs, team)
end

------------------------------------------------------------ ДАННЫЕ
local S = {} -- рантайм-состояние игроков

local function defaultData()
	return {Credits = 200, Owned = {}, Slot1 = "Рейд-47", Slot2 = "Р-17", Role = "Assault", Settings = {}, Donated = 0}
end

local function loadData(plr)
	local def = defaultData()
	local ok, d = pcall(function() return store:GetAsync("p_" .. plr.UserId) end)
	if ok and type(d) == "table" then
		for k, v in pairs(def) do if d[k] == nil then d[k] = v end end
		return d
	end
	return def
end

local function saveData(plr)
	local st = S[plr]; if not st then return end
	pcall(function() store:SetAsync("p_" .. plr.UserId, st.data) end)
end

local function notify(plr, text, color)
	R.Notify:FireClient(plr, text, color or Color3.fromRGB(255, 200, 80))
end

local function addCredits(plr, n)
	local st = S[plr]; if not st then return end
	st.data.Credits = math.max(0, st.data.Credits + n)
	local ls = plr:FindFirstChild("leaderstats")
	if ls then ls.Credits.Value = st.data.Credits end
end

local function owns(plr, name)
	local cfg, st = Config.Weapons[name], S[plr]
	if not cfg or not st then return false end
	if cfg.VIPOnly then return st.vip == true end
	return cfg.Price == 0 or st.data.Owned[name] == true
end

local function priceOf(plr, name)
	local cfg = Config.Weapons[name]
	local deal = Config.GetWeeklyDeal()
	local p = cfg.Price * (1 - (deal.Discounts[name] or 0))
	if S[plr].vip then p *= 0.8 end
	return math.floor(p)
end

local function clampNum(v, a, b, def)
	if type(v) == "number" and v == v then return math.clamp(v, a, b) end
	return def
end

local function sanitize(s)
	local out = {}
	if type(s) ~= "table" then return out end
	out.FOV = clampNum(s.FOV, 60, 110, 80)
	out.CrosshairSize = clampNum(s.CrosshairSize, 4, 30, 10)
	out.MobileScale = clampNum(s.MobileScale, 0.6, 1.6, 1)
	out.MobileOpacity = clampNum(s.MobileOpacity, 0.2, 1, 0.6)
	out.Hitmarker = s.Hitmarker ~= false
	out.FirstPerson = s.FirstPerson ~= false
	if type(s.CrosshairColor) == "table" then
		out.CrosshairColor = {clampNum(s.CrosshairColor[1],0,255,0), clampNum(s.CrosshairColor[2],0,255,255), clampNum(s.CrosshairColor[3],0,255,0)}
	end
	if type(s.Keys) == "table" then
		out.Keys = {}
		for action in pairs(Config.DefaultKeys) do
			local k = s.Keys[action]
			if type(k) == "string" and #k <= 20 then out.Keys[action] = k end
		end
	end
	out.MobilePos = {}
	if type(s.MobilePos) == "table" then
		for name, p in pairs(s.MobilePos) do
			if type(name) == "string" and #name <= 12 and type(p) == "table" then
				out.MobilePos[name] = {clampNum(p[1],0,1,0.5), clampNum(p[2],0,1,0.5)}
			end
		end
	end
	return out
end

------------------------------------------------------------ ОРУЖИЕ (внешний вид + состояние)
local function weld(a, b, c0)
	local w = Instance.new("Weld"); w.Part0 = a; w.Part1 = b; w.C0 = c0; w.Parent = a
end

local function buildGun(char, name)
	local old = char:FindFirstChild("GunModel"); if old then old:Destroy() end
	local cfg = Config.Weapons[name]; if not cfg then return end
	local hand = char:FindFirstChild("RightHand") or char:FindFirstChild("Right Arm"); if not hand then return end
	local m = Instance.new("Model"); m.Name = "GunModel"
	local function part(n, size, color, mat)
		local p = Instance.new("Part"); p.Name = n; p.Size = size; p.Color = color; p.Material = mat or Enum.Material.Metal
		p.CanCollide = false; p.Massless = true; p.Parent = m; return p
	end
	local z = cfg.Size.Z
	local body = part("Handle", cfg.Size, cfg.Color)
	local barrel = part("Barrel", Vector3.new(0.16, 0.16, 0.7), Color3.fromRGB(25, 25, 25))
	local mag = part("Mag", Vector3.new(0.3, 0.7, 0.45), Color3.fromRGB(30, 30, 30))
	local stock = part("Stock", Vector3.new(0.3, 0.5, 0.9), cfg.Color, Enum.Material.SmoothPlastic)
	local muzzle = part("Muzzle", Vector3.new(0.1, 0.1, 0.1), Color3.new(), Enum.Material.SmoothPlastic); muzzle.Transparency = 1
	m.Parent = char
	weld(hand, body, CFrame.new(0, -0.2, -(z / 2 - 0.4)))
	weld(body, barrel, CFrame.new(0, 0.05, -z / 2 - 0.35))
	weld(body, mag, CFrame.new(0, -0.55, 0.2))
	weld(body, stock, CFrame.new(0, -0.05, z / 2 + 0.4))
	weld(body, muzzle, CFrame.new(0, 0.05, -z / 2 - 0.75))
end

local function sync(plr)
	local st = S[plr]; if not st then return end
	local a = st.ammo[st.cur]
	plr:SetAttribute("Weapon", st.slots[st.cur])
	plr:SetAttribute("Slot", st.cur)
	plr:SetAttribute("Mag", a and a.mag or 0)
	plr:SetAttribute("Reserve", a and a.reserve or 0)
	plr:SetAttribute("Reloading", st.reloading or false)
end

------------------------------------------------------------ КОСТЮМЫ
local function applyOutfit(plr, char, idx)
	local o = Config.Outfits[idx]; if not o or not char then return end
	for _, c in ipairs(char:GetChildren()) do
		if c:IsA("Shirt") or c:IsA("Pants") or c:IsA("ShirtGraphic") or c:IsA("Accessory") then c:Destroy() end
	end
	local bc = char:FindFirstChildOfClass("BodyColors") or Instance.new("BodyColors", char)
	for _, k in ipairs({"TorsoColor3", "LeftArmColor3", "RightArmColor3"}) do bc[k] = o.Shirt end
	for _, k in ipairs({"LeftLegColor3", "RightLegColor3"}) do bc[k] = o.Pants end
	local head = char:FindFirstChild("Head")
	for _, n in ipairs({"Helmet", "HelmetStripe"}) do local x = char:FindFirstChild(n); if x then x:Destroy() end end
	if head then
		local h = Instance.new("Part"); h.Name = "Helmet"; h.Size = Vector3.new(1.5, 0.7, 1.5)
		h.Color = o.Helmet; h.Material = Enum.Material.Metal; h.CanCollide = false; h.Massless = true; h.Parent = char
		weld(head, h, CFrame.new(0, 0.4, 0))
		local s = Instance.new("Part"); s.Name = "HelmetStripe"; s.Size = Vector3.new(1.55, 0.15, 1.55)
		s.Color = plr.Team and plr.Team.TeamColor.Color or Color3.new(1, 1, 1)
		s.Material = Enum.Material.SmoothPlastic; s.CanCollide = false; s.Massless = true; s.Parent = char
		weld(head, s, CFrame.new(0, 0.2, 0))
	end
end

------------------------------------------------------------ УРОН / ВЗРЫВЫ / КОМАНДНЫЙ СЧЁТ
local function damage(att, vic, hum, amount, weapon, head, fromPos)
	local vst = S[vic]
	if not vst or hum.Health <= 0 or not vic.Character or vic.Character:FindFirstChildOfClass("ForceField") then return end
	vst.lastHit = {att = att, weapon = weapon, head = head, t = os.clock()}
	hum:TakeDamage(amount)
	if att ~= vic then
		R.HitMark:FireClient(att, head, hum.Health <= 0)
		local ah = att.Character and att.Character:FindFirstChild("Head")
		local pos = fromPos or (ah and ah.Position)
		if pos then R.Damaged:FireClient(vic, pos) end
	end
end

local function explode(pos, radius, maxDmg, att, weapon)
	local e = Instance.new("Explosion")
	e.Position = pos; e.BlastRadius = radius; e.BlastPressure = 0; e.DestroyJointRadiusPercent = 0; e.Parent = workspace
	for _, p in ipairs(Players:GetPlayers()) do
		local c = p.Character
		local r = c and c:FindFirstChild("HumanoidRootPart")
		local h = c and c:FindFirstChildOfClass("Humanoid")
		if r and h and h.Health > 0 and (p.Team ~= att.Team or p == att) then
			local dist = (r.Position - pos).Magnitude
			if dist <= radius then
				local dmg = maxDmg * (1 - dist / radius * 0.8)
				if p == att then dmg *= 0.5 end
				damage(att, p, h, dmg, weapon, false, pos)
			end
		end
	end
end

local roundOver = false
local function addTeamScore(team)
	if roundOver then return end
	local s = (team:GetAttribute("Score") or 0) + 1
	team:SetAttribute("Score", s)
	if s >= Config.ScoreToWin then
		roundOver = true
		R.Notify:FireAllClients("ПОБЕДА: " .. team.Name .. "!", team.TeamColor.Color)
		task.delay(8, function()
			for _, t in ipairs(teamObjs) do t:SetAttribute("Score", 0) end
			roundOver = false
			for _, p in ipairs(Players:GetPlayers()) do
				local st = S[p]
				if st and st.deployed then p:LoadCharacter() end
			end
		end)
	end
end

local function award(killer, head)
	local st = S[killer]; if not st then return end
	local deal = Config.GetWeeklyDeal()
	local gain = math.floor((25 + (head and 10 or 0)) * deal.CreditMult * (st.vip and 2 or 1))
	addCredits(killer, gain)
	local ls = killer:FindFirstChild("leaderstats")
	if ls then ls.Kills.Value += 1 end
	if killer.Team then addTeamScore(killer.Team) end
end

------------------------------------------------------------ ПАТРОНЫ (дроп с убитых + ящики) И КОСТЮМЫ
local function dropAmmo(char)
	local root = char:FindFirstChild("HumanoidRootPart"); if not root then return end
	local p = Instance.new("Part"); p.Name = "AmmoDrop"; p.Size = Vector3.new(1.6, 1, 1.2)
	p.Color = Color3.fromRGB(80, 95, 60); p.Material = Enum.Material.Metal; p.Position = root.Position
	p.CanQuery = false; p:SetAttribute("OneShot", true); p:SetAttribute("Label", "Патроны")
	p.Parent = effects
	CS:AddTag(p, "AmmoCrate")
	Debris:AddItem(p, 40)
end

local function setupCrate(part)
	if part:FindFirstChildOfClass("ProximityPrompt") then return end
	local outfit = CS:HasTag(part, "OutfitCrate")
	local pp = Instance.new("ProximityPrompt")
	pp.ActionText = outfit and "Надеть костюм" or "Взять патроны"
	pp.ObjectText = part:GetAttribute("Label") or ""
	pp.HoldDuration = 0.4; pp.MaxActivationDistance = 8; pp.RequiresLineOfSight = false
	pp.Parent = part
	pp.Triggered:Connect(function(plr)
		local st = S[plr]; local char = plr.Character
		local hum = char and char:FindFirstChildOfClass("Humanoid")
		if not st or not hum or hum.Health <= 0 then return end
		if outfit then
			st.outfit = part:GetAttribute("Outfit")
			applyOutfit(plr, char, st.outfit)
			notify(plr, "Костюм: " .. Config.Outfits[st.outfit].Name)
		else
			local changed = false
			for i, name in ipairs(st.slots) do
				local c, a = Config.Weapons[name], st.ammo[i]
				local new = math.min(c.Reserve, a.reserve + c.Mag * 2)
				if new ~= a.reserve then a.reserve = new; changed = true end
			end
			if not changed then notify(plr, "Патроны полные"); return end
			sync(plr); notify(plr, "Патроны пополнены")
			if part:GetAttribute("OneShot") then part:Destroy()
			else
				pp.Enabled = false
				task.delay(20, function() if pp.Parent then pp.Enabled = true end end)
			end
		end
	end)
end
for _, tag in ipairs({"AmmoCrate", "OutfitCrate"}) do
	CS:GetInstanceAddedSignal(tag):Connect(setupCrate)
	for _, p in ipairs(CS:GetTagged(tag)) do setupCrate(p) end
end

------------------------------------------------------------ СМЕРТЬ И РЕСПАУН
local function teamColor(p) return p.Team and p.Team.TeamColor.Color or Color3.new(1, 1, 1) end

local function onDied(plr, char)
	local st = S[plr]; if not st then return end
	local ls = plr:FindFirstChild("leaderstats")
	if ls then ls.Deaths.Value += 1 end
	if st.drone then st.drone:Destroy(); st.drone = nil; R.DroneEnd:FireClient(plr) end
	local lh = st.lastHit
	local killer = lh and lh.att.Parent and os.clock() - lh.t < 10 and lh.att or nil
	if killer and killer ~= plr then
		award(killer, lh.head)
		R.KillFeed:FireAllClients(killer.Name, teamColor(killer), plr.Name, teamColor(plr), lh.weapon, lh.head)
	else
		R.KillFeed:FireAllClients("", Color3.new(1, 1, 1), plr.Name, teamColor(plr), "", false)
	end
	dropAmmo(char)
	task.delay(Config.RespawnTime, function()
		if plr.Parent and st.deployed and (not plr.Character or plr.Character == char) then plr:LoadCharacter() end
	end)
end

local function onCharacter(plr, char)
	local st = S[plr]; if not st then return end
	local hum = char:WaitForChild("Humanoid")
	char:WaitForChild("HumanoidRootPart")
	if not plr:HasAppearanceLoaded() then plr.CharacterAppearanceLoaded:Wait() end
	if not char.Parent then return end

	local d = st.data
	local role = Config.Roles[d.Role] or Config.Roles.Assault
	hum.MaxHealth = role.Health; hum.Health = role.Health; hum.WalkSpeed = role.Speed
	char:SetAttribute("BaseSpeed", role.Speed)
	hum.DisplayName = (st.vip and "[VIP] " or "") .. plr.DisplayName

	if not st.outfit then
		for i, t in ipairs(Config.Teams) do
			if plr.Team and plr.Team.Name == t.Name then st.outfit = t.DefaultOutfit end
		end
	end
	applyOutfit(plr, char, st.outfit or 1)

	-- проверяем, что выбранное оружие доступно
	for slot = 1, 2 do
		local n = d["Slot" .. slot]
		if not (Config.Weapons[n] and Config.Weapons[n].Slot == slot and owns(plr, n)) then
			d["Slot" .. slot] = slot == 1 and "Рейд-47" or "Р-17"
		end
	end
	st.slots = {d.Slot1, d.Slot2}
	st.ammo = {}
	for i, name in ipairs(st.slots) do
		local c = Config.Weapons[name]
		st.ammo[i] = {mag = c.Mag, reserve = c.Reserve}
	end
	st.cur = 1; st.reloading = false; st.rid = nil; st.drone = nil; st.abReady = 0; st.lastHit = nil
	buildGun(char, st.slots[1]); sync(plr)
	plr:SetAttribute("AbilityName", Config.Abilities[role.Ability].Title)
	plr:SetAttribute("AbilityReadyAt", 0)

	local ff = Instance.new("ForceField"); ff.Visible = false; ff.Parent = char
	Debris:AddItem(ff, 3)
	hum.Died:Connect(function() onDied(plr, char) end)
end

------------------------------------------------------------ СТРЕЛЬБА
local function spread(dir, deg)
	local cf = CFrame.lookAt(Vector3.zero, dir) * CFrame.Angles(0, 0, math.random() * math.pi * 2)
		* CFrame.Angles(math.rad(deg * math.random()), 0, 0)
	return cf.LookVector
end

R.Fire.OnServerEvent:Connect(function(plr, origin, dir)
	local st, char = S[plr], plr.Character
	if not st or not st.deployed or not char then return end
	local hum = char:FindFirstChildOfClass("Humanoid")
	if not hum or hum.Health <= 0 or st.drone then return end
	if typeof(origin) ~= "Vector3" or typeof(dir) ~= "Vector3" or dir.Magnitude < 0.1 then return end
	local head = char:FindFirstChild("Head")
	if not head or (head.Position - origin).Magnitude > 15 then return end

	local name = st.slots[st.cur]; local cfg = Config.Weapons[name]; local a = st.ammo[st.cur]
	local now = os.clock()
	if st.reloading or a.mag <= 0 or now - st.last < 60 / cfg.RPM - 0.03 then return end
	st.last = now; a.mag -= 1

	local params = RaycastParams.new()
	params.FilterType = Enum.RaycastFilterType.Exclude
	params.FilterDescendantsInstances = {char, effects}
	local gun = char:FindFirstChild("GunModel")
	local muzzle = gun and gun:FindFirstChild("Muzzle")
	local from = muzzle and muzzle.Position or head.Position
	local unit = dir.Unit

	for _ = 1, cfg.Pellets do
		local d = spread(unit, cfg.Spread)
		local res = workspace:Raycast(origin, d * cfg.Range, params)
		local hitPos = res and res.Position or origin + d * cfg.Range
		R.Tracer:FireAllClients(from, hitPos)
		if res then
			local model = res.Instance:FindFirstAncestorOfClass("Model")
			local th = model and model:FindFirstChildOfClass("Humanoid")
			local tp = model and Players:GetPlayerFromCharacter(model)
			if th and tp and tp.Team ~= plr.Team then
				local isHead = res.Instance.Name == "Head"
				local dmg = cfg.Damage * (isHead and cfg.Head or 1)
				local dist = (hitPos - origin).Magnitude
				if dist > cfg.Range * 0.5 then dmg *= 1 - 0.4 * ((dist - cfg.Range * 0.5) / (cfg.Range * 0.5)) end
				damage(plr, tp, th, dmg, name, isHead)
			end
		end
	end
	sync(plr)
end)

R.Reload.OnServerEvent:Connect(function(plr)
	local st = S[plr]; if not st or not st.deployed then return end
	local cfg = Config.Weapons[st.slots[st.cur]]; local a = st.ammo[st.cur]
	if st.reloading or a.mag >= cfg.Mag or a.reserve <= 0 then return end
	st.reloading = true; local id = os.clock(); st.rid = id; sync(plr)
	task.delay(cfg.Reload, function()
		if st.rid ~= id or not st.reloading then return end
		local take = math.min(cfg.Mag - a.mag, a.reserve)
		a.mag += take; a.reserve -= take; st.reloading = false
		sync(plr)
	end)
end)

R.Equip.OnServerEvent:Connect(function(plr, slot)
	local st, char = S[plr], plr.Character
	if not st or not char or (slot ~= 1 and slot ~= 2) or st.drone then return end
	local hum = char:FindFirstChildOfClass("Humanoid")
	if not hum or hum.Health <= 0 or st.cur == slot then return end
	st.cur = slot; st.reloading = false; st.rid = nil
	buildGun(char, st.slots[slot]); sync(plr)
end)

------------------------------------------------------------ СПОСОБНОСТИ (клавиша 3)
local function detonateDrone(plr)
	local st = S[plr]; local d = st and st.drone; if not d then return end
	st.drone = nil
	explode(d.Position, 14, 110, plr, "FPV-дрон")
	d:Destroy()
	R.DroneEnd:FireClient(plr)
end

R.DroneDetonate.OnServerEvent:Connect(detonateDrone)

R.Ability.OnServerEvent:Connect(function(plr)
	local st, char = S[plr], plr.Character
	if not st or not st.deployed or not char then return end
	local hum = char:FindFirstChildOfClass("Humanoid"); local root = char:FindFirstChild("HumanoidRootPart")
	if not hum or not root or hum.Health <= 0 then return end
	local role = Config.Roles[st.data.Role] or Config.Roles.Assault
	local ab = role.Ability; local abCfg = Config.Abilities[ab]
	local now = os.clock()
	if st.drone or now < (st.abReady or 0) then return end
	local deal = Config.GetWeeklyDeal()
	local cd = abCfg.Cooldown
	if ab == "FPV" and deal.FPVCooldown then cd *= deal.FPVCooldown end
	st.abReady = now + cd
	plr:SetAttribute("AbilityReadyAt", workspace:GetServerTimeNow() + cd)
	local look = root.CFrame.LookVector

	if ab == "Heal" then
		hum.Health = math.min(hum.MaxHealth, hum.Health + 50)
		notify(plr, "+50 здоровья", Color3.fromRGB(120, 255, 120))
	elseif ab == "Frag" then
		local g = Instance.new("Part"); g.Shape = Enum.PartType.Ball; g.Size = Vector3.new(1, 1, 1)
		g.Color = Color3.fromRGB(60, 80, 50); g.Material = Enum.Material.Metal
		g.Position = root.Position + look * 2 + Vector3.new(0, 1.5, 0); g.Parent = effects
		g:SetNetworkOwner(nil)
		g.AssemblyLinearVelocity = look * 60 + Vector3.new(0, 28, 0)
		task.delay(2.5, function()
			local pos = g.Position; g:Destroy()
			explode(pos, 18, 120, plr, "Граната")
		end)
	elseif ab == "Smoke" then
		local p = Instance.new("Part"); p.Anchored = true; p.CanCollide = false; p.CanQuery = false; p.CanTouch = false
		p.Transparency = 1; p.Size = Vector3.new(2, 2, 2); p.Position = root.Position + look * 14 + Vector3.new(0, 2, 0)
		local sm = Instance.new("Smoke"); sm.Size = 25; sm.Opacity = 0.95; sm.RiseVelocity = 2
		sm.Color = Color3.fromRGB(190, 190, 190); sm.Parent = p
		p.Parent = effects; Debris:AddItem(p, 14)
	elseif ab == "FPV" then
		local drone = Instance.new("Part"); drone.Name = "FPVDrone"; drone.Size = Vector3.new(1.4, 0.5, 1.4)
		drone.Color = Color3.fromRGB(30, 30, 30); drone.Material = Enum.Material.Metal
		drone.Position = root.Position + Vector3.new(0, 5, 0) + look * 3
		local led = Instance.new("PointLight"); led.Color = Color3.fromRGB(255, 60, 60); led.Range = 8; led.Parent = drone
		local bv = Instance.new("BodyVelocity"); bv.MaxForce = Vector3.new(1e5, 1e5, 1e5); bv.Velocity = Vector3.zero; bv.Parent = drone
		drone.Parent = effects
		drone:SetNetworkOwner(plr)
		st.drone = drone
		R.DroneStart:FireClient(plr, drone)
		drone.Touched:Connect(function(hit)
			if hit:IsDescendantOf(char) or hit.Parent == effects then return end
			if st.drone == drone then detonateDrone(plr) end
		end)
		task.delay(25, function() if st.drone == drone then detonateDrone(plr) end end)
	end
end)

------------------------------------------------------------ МЕНЮ: ВХОД В БОЙ, РОЛИ, ЭКИПИРОВКА, МАГАЗИН
R.Deploy.OnServerEvent:Connect(function(plr)
	local st = S[plr]; if not st then return end
	local hum = plr.Character and plr.Character:FindFirstChildOfClass("Humanoid")
	if st.deployed and hum and hum.Health > 0 then return end
	if st.deployed then return end -- уже в игре, ждёт респауна
	st.deployed = true
	plr:LoadCharacter()
	local deal = Config.GetWeeklyDeal()
	notify(plr, "Акция недели: " .. deal.Title)
end)

R.SetRole.OnServerEvent:Connect(function(plr, key)
	local st = S[plr]
	if not st or type(key) ~= "string" or not Config.Roles[key] then return end
	st.data.Role = key
	notify(plr, "Роль: " .. Config.Roles[key].Title .. " (со следующего возрождения)")
end)

R.SetLoadout.OnServerEvent:Connect(function(plr, slot, name)
	local st = S[plr]
	if not st or (slot ~= 1 and slot ~= 2) or type(name) ~= "string" then return end
	local cfg = Config.Weapons[name]
	if not cfg or cfg.Slot ~= slot or not owns(plr, name) then return end
	st.data["Slot" .. slot] = name
	notify(plr, name .. " (со следующего возрождения)")
end)

R.SaveSettings.OnServerEvent:Connect(function(plr, s)
	local st = S[plr]; if not st then return end
	st.data.Settings = sanitize(s)
end)

R.Buy.OnServerInvoke = function(plr, name)
	local st, cfg = S[plr], Config.Weapons[tostring(name)]
	if not st or not cfg then return false, "Нет такого предмета" end
	if cfg.VIPOnly then return false, "Только для VIP" end
	if owns(plr, name) then return false, "Уже куплено" end
	local price = priceOf(plr, name)
	if st.data.Credits < price then return false, "Недостаточно кредитов" end
	addCredits(plr, -price)
	st.data.Owned[name] = true
	return true, "Куплено: " .. name
end

R.GetData.OnServerInvoke = function(plr)
	local st = S[plr]; if not st then return nil end
	local d = st.data
	local deal, left = Config.GetWeeklyDeal()
	local prices, owned = {}, {}
	for name in pairs(Config.Weapons) do prices[name] = priceOf(plr, name); owned[name] = owns(plr, name) end
	return {
		Credits = d.Credits, Owned = owned, Prices = prices, Slot1 = d.Slot1, Slot2 = d.Slot2,
		Role = d.Role, VIP = st.vip or false,
		Deal = {Title = deal.Title, Discounts = deal.Discounts, CreditMult = deal.CreditMult},
		TimeLeft = left, Settings = d.Settings,
	}
end

------------------------------------------------------------ ДОНАТ, VIP, "ПОДДЕРЖАТЬ МЕНЯ"
local function setVIP(plr)
	local st = S[plr]; if not st then return end
	st.vip = true; plr:SetAttribute("VIP", true)
	notify(plr, "VIP активирован! x2 кредиты, -20% в магазине", Color3.fromRGB(255, 215, 0))
end

MPS.PromptGamePassPurchaseFinished:Connect(function(plr, id, purchased)
	if purchased and id == Config.VIPGamePassId and id ~= 0 then setVIP(plr) end
end)

MPS.ProcessReceipt = function(info)
	local plr = Players:GetPlayerByUserId(info.PlayerId)
	local st = plr and S[plr]
	if not st then return Enum.ProductPurchaseDecision.NotProcessedYet end
	for _, p in ipairs(Config.Products.Credits) do
		if p.Id ~= 0 and p.Id == info.ProductId then
			addCredits(plr, p.Amount); saveData(plr)
			notify(plr, "+" .. p.Amount .. " кредитов", Color3.fromRGB(120, 255, 120))
			return Enum.ProductPurchaseDecision.PurchaseGranted
		end
	end
	for _, p in ipairs(Config.Products.Support) do
		if p.Id ~= 0 and p.Id == info.ProductId then
			st.data.Donated += p.Robux
			addCredits(plr, p.Robux * 10)       -- бонус за поддержку
			plr:SetAttribute("Supporter", true)
			saveData(plr)
			notify(plr, "Спасибо за поддержку! Бонус: +" .. p.Robux * 10 .. " кредитов", Color3.fromRGB(255, 140, 200))
			return Enum.ProductPurchaseDecision.PurchaseGranted
		end
	end
	return Enum.ProductPurchaseDecision.NotProcessedYet
end

------------------------------------------------------------ ИГРОКИ
local function onPlayer(plr)
	if S[plr] then return end
	local d = loadData(plr)
	S[plr] = {data = d, deployed = false, cur = 1, slots = {d.Slot1, d.Slot2}, ammo = {}, last = 0}
	local st = S[plr]

	local ls = Instance.new("Folder"); ls.Name = "leaderstats"
	for _, n in ipairs({"Kills", "Deaths", "Credits"}) do
		local v = Instance.new("IntValue"); v.Name = n; v.Parent = ls
	end
	ls.Credits.Value = d.Credits
	ls.Parent = plr

	local best, bc = nil, math.huge
	for _, t in ipairs(teamObjs) do
		local c = #t:GetPlayers()
		if c < bc then best = t; bc = c end
	end
	plr.Team = best

	if Config.VIPGamePassId ~= 0 then
		local ok, has = pcall(function() return MPS:UserOwnsGamePassAsync(plr.UserId, Config.VIPGamePassId) end)
		if ok and has then st.vip = true; plr:SetAttribute("VIP", true) end
	end
	plr.CharacterAdded:Connect(function(c) onCharacter(plr, c) end)
end

Players.PlayerAdded:Connect(onPlayer)
for _, p in ipairs(Players:GetPlayers()) do task.spawn(onPlayer, p) end

Players.PlayerRemoving:Connect(function(plr)
	saveData(plr)
	S[plr] = nil
end)

game:BindToClose(function()
	for _, p in ipairs(Players:GetPlayers()) do saveData(p) end
end)

task.spawn(function()
	while true do
		task.wait(120)
		for _, p in ipairs(Players:GetPlayers()) do saveData(p) end
	end
end)
```

---

## ЧАСТЬ 4. `MapBuilder` (Script в ServerScriptService)

Строит карту «зона боевых действий»: разрушенные здания, воронки, мешки с песком, сгоревшие машины, бочки с огнём, дым, туман, спавны команд, ящики с патронами и ящики с костюмами.

```lua
local Lighting = game:GetService("Lighting")
local CS = game:GetService("CollectionService")
local RS = game:GetService("ReplicatedStorage")
local Config = require(RS:WaitForChild("Config"))

local rng = Random.new(1337)
local M = Enum.Material

local map = Instance.new("Folder"); map.Name = "Map"; map.Parent = workspace
local effects = workspace:FindFirstChild("Effects") or Instance.new("Folder")
effects.Name = "Effects"; effects.Parent = workspace

local function P(name, size, cf, color, mat, parent)
	local p = Instance.new("Part")
	p.Name = name; p.Anchored = true; p.Size = size; p.CFrame = cf; p.Color = color
	p.Material = mat or M.Concrete
	p.TopSurface = Enum.SurfaceType.Smooth; p.BottomSurface = Enum.SurfaceType.Smooth
	p.Parent = parent or map
	return p
end
local function jitter(r, g, b, a)
	local v = rng:NextInteger(-a, a)
	return Color3.fromRGB(math.clamp(r + v, 0, 255), math.clamp(g + v, 0, 255), math.clamp(b + v, 0, 255))
end
local function smokeAt(pos, size)
	local p = Instance.new("Part"); p.Anchored = true; p.CanCollide = false; p.CanQuery = false; p.CanTouch = false
	p.Transparency = 1; p.Size = Vector3.new(1, 1, 1); p.Position = pos; p.Parent = map
	local s = Instance.new("Smoke"); s.Size = size; s.Opacity = 0.45; s.RiseVelocity = 8; s.Color = Color3.fromRGB(55, 55, 55); s.Parent = p
	return p
end

------------------------------------------------------------ ЗЕМЛЯ И ГРАНИЦЫ
P("Ground", Vector3.new(600, 2, 600), CFrame.new(0, -1, 0), Color3.fromRGB(88, 80, 68), M.Ground)
for _, w in ipairs({{0, -300, 600, 4}, {0, 300, 600, 4}, {-300, 0, 4, 600}, {300, 0, 4, 600}}) do
	P("Border", Vector3.new(w[3], 40, w[4]), CFrame.new(w[1], 20, w[2]), Color3.fromRGB(50, 48, 46), M.Concrete)
end

------------------------------------------------------------ ЭЛЕМЕНТЫ
local function crater(x, z, d)
	local c = P("Crater", Vector3.new(0.3, d, d), CFrame.new(x, 0.08, z) * CFrame.Angles(0, 0, math.pi / 2), Color3.fromRGB(40, 35, 30), M.Mud)
	c.Shape = Enum.PartType.Cylinder; c.CanCollide = false
	for i = 1, 8 do
		local a = i / 8 * math.pi * 2
		local s = rng:NextNumber(0.8, 2)
		P("Rubble", Vector3.new(s, s * 0.7, s),
			CFrame.new(x + math.cos(a) * d / 2, s * 0.3, z + math.sin(a) * d / 2) * CFrame.Angles(rng:NextNumber(0, 3), rng:NextNumber(0, 3), 0),
			jitter(100, 95, 88, 12), M.Slate)
	end
end

local function barrel(x, z)
	local rust = rng:NextNumber() < 0.5
	local b = P("Barrel", Vector3.new(3, 2.2, 2.2), CFrame.new(x, 1.5, z) * CFrame.Angles(0, 0, math.pi / 2),
		rust and Color3.fromRGB(140, 62, 40) or Color3.fromRGB(62, 82, 60), M.CorrodedMetal)
	b.Shape = Enum.PartType.Cylinder
	if rng:NextNumber() < 0.3 then
		local f = Instance.new("Fire"); f.Size = 6; f.Heat = 5; f.Parent = b
		smokeAt(Vector3.new(x, 4, z), 8)
	end
end

local function sandbags(x, z, yaw, n)
	local base = CFrame.new(x, 0, z) * CFrame.Angles(0, math.rad(yaw), 0)
	for row = 1, 2 do
		for i = 1, n do
			P("Sandbag", Vector3.new(3.2, 1.2, 1.6),
				base * CFrame.new((i - n / 2 - 0.5) * 3 + (row % 2) * 1.5, 0.6 + (row - 1) * 1.2, 0),
				jitter(170, 150, 110, 10), M.Fabric)
		end
	end
end

local function barrier(x, z, yaw)
	P("Barrier", Vector3.new(6, 3, 1.6), CFrame.new(x, 1.5, z) * CFrame.Angles(0, math.rad(yaw), 0), jitter(120, 120, 118, 10), M.Concrete)
end

local function wreck(x, z, yaw)
	local base = CFrame.new(x, 0, z) * CFrame.Angles(0, math.rad(yaw), 0)
	local dark = Color3.fromRGB(42, 40, 38)
	P("WreckBody", Vector3.new(6, 2, 13), base * CFrame.new(0, 2, 0), dark, M.CorrodedMetal)
	P("WreckCab", Vector3.new(5.6, 2.2, 5), base * CFrame.new(0, 4.1, -3), Color3.fromRGB(55, 50, 46), M.CorrodedMetal)
	for _, wx in ipairs({-3.1, 3.1}) do
		for _, wz in ipairs({-4, 4}) do
			local w = P("Wheel", Vector3.new(1, 2.4, 2.4), base * CFrame.new(wx, 1.2, wz), Color3.fromRGB(15, 15, 15), M.Rubber)
			w.Shape = Enum.PartType.Cylinder
		end
	end
	smokeAt((base * CFrame.new(0, 5, 2)).Position, 10)
end

local function deadTree(x, z)
	local h = rng:NextNumber(8, 12)
	local brown = Color3.fromRGB(58, 44, 34)
	P("Trunk", Vector3.new(1, h, 1), CFrame.new(x, h / 2, z), brown, M.Wood)
	for i = 1, 2 do
		P("Branch", Vector3.new(0.4, 4, 0.4), CFrame.new(x, h - 1.5 * i, z) * CFrame.Angles(0, i * 2, math.rad(rng:NextInteger(35, 60))) * CFrame.new(0, 2, 0), brown, M.Wood)
	end
end

------------------------------------------------------------ РАЗРУШЕННЫЕ ЗДАНИЯ
local rects = {}
local function ruin(cx, cz, w, d, h, yaw)
	table.insert(rects, {cx, cz, math.max(w, d) / 2 + 8})
	local model = Instance.new("Model"); model.Name = "Ruin"; model.Parent = map
	local base = CFrame.new(cx, 0, cz) * CFrame.Angles(0, math.rad(yaw), 0)
	local B = 4
	local function wall(len, offset, rotY, doorway)
		local n = math.floor(len / B)
		for i = 1, n do
			for j = 1, math.floor(h / B) do
				local skip = rng:NextNumber() < (j - 1) * 0.22 + 0.02
				if j == 2 and i % 3 == 0 then skip = true end                  -- окна
				if doorway and j <= 2 and math.abs(i - n / 2 - 0.5) < 1.1 then skip = true end -- дверь
				if not skip then
					local x = (i - 0.5) * B - len / 2
					P("Wall", Vector3.new(B, B, 1.2),
						base * CFrame.new(offset) * CFrame.Angles(0, rotY, 0) * CFrame.new(x, (j - 0.5) * B, 0),
						jitter(135, 118, 102, 14), j % 2 == 0 and M.Brick or M.Concrete, model)
				end
			end
		end
	end
	wall(w, Vector3.new(0, 0, -d / 2), 0, true)
	wall(w, Vector3.new(0, 0, d / 2), 0, false)
	wall(d, Vector3.new(-w / 2, 0, 0), math.pi / 2, false)
	wall(d, Vector3.new(w / 2, 0, 0), math.pi / 2, true)
	-- куски крыши и укрытия внутри
	for _ = 1, 2 do
		P("Roof", Vector3.new(8, 0.8, 8), base * CFrame.new(rng:NextNumber(-w / 3, w / 3), h, rng:NextNumber(-d / 3, d / 3)) * CFrame.Angles(rng:NextNumber(-0.1, 0.1), 0, 0), jitter(90, 90, 88, 8), M.Concrete, model)
	end
	for _ = 1, 3 do
		P("Cover", Vector3.new(rng:NextNumber(2, 4), 2.4, 2), base * CFrame.new(rng:NextNumber(-w / 3, w / 3), 1.2, rng:NextNumber(-d / 3, d / 3)), Color3.fromRGB(96, 70, 48), M.Wood, model)
	end
end

local buildings = {
	{-90, -60, 24, 18, 12, 0}, {80, -40, 20, 20, 12, 15}, {-30, 10, 28, 16, 16, 0},
	{110, 60, 22, 16, 12, 90}, {-120, 70, 20, 20, 8, 0}, {20, -110, 26, 16, 12, 0},
}
for _, b in ipairs(buildings) do
	ruin(b[1], b[2], b[3], b[4], b[5], b[6])
	ruin(-b[1], -b[2], b[3], b[4], b[5], b[6] + 180) -- зеркальная копия для баланса
end

local function free(x, z)
	for _, r in ipairs(rects) do
		if math.abs(x - r[1]) < r[3] and math.abs(z - r[2]) < r[3] then return false end
	end
	return true
end

------------------------------------------------------------ РАЗБРОС УКРЫТИЙ
for _ = 1, 70 do
	local x, z = rng:NextInteger(-270, 270), rng:NextInteger(-185, 185)
	if free(x, z) then
		local k = rng:NextInteger(1, 7)
		if k == 1 then crater(x, z, rng:NextInteger(10, 20))
		elseif k == 2 then barrel(x, z)
		elseif k == 3 then sandbags(x, z, rng:NextInteger(0, 180), 4)
		elseif k == 4 then barrier(x, z, rng:NextInteger(0, 180))
		elseif k == 5 then wreck(x, z, rng:NextInteger(0, 180))
		elseif k == 6 then deadTree(x, z)
		else sandbags(x, z, rng:NextInteger(0, 180), 3) end
	end
end
for _ = 1, 6 do smokeAt(Vector3.new(rng:NextInteger(-200, 200), 3, rng:NextInteger(-150, 150)), 18) end

------------------------------------------------------------ СПАВНЫ КОМАНД
for ti, t in ipairs(Config.Teams) do
	local z = ti == 1 and -240 or 240
	for i = 1, 4 do
		local s = Instance.new("SpawnLocation")
		s.Anchored = true; s.Size = Vector3.new(8, 1, 8); s.Position = Vector3.new((i - 2.5) * 18, 0.5, z)
		s.Neutral = false; s.TeamColor = t.Color; s.AllowTeamChangeOnTouch = false; s.Duration = 0
		s.Transparency = 0.5; s.Material = M.Metal; s.Color = t.Color.Color; s.Parent = map
	end
	local dir = ti == 1 and 1 or -1
	for _, x in ipairs({-100, -50, 50, 100}) do sandbags(x, z + dir * 28, 0, 6) end
	P("FlagPole", Vector3.new(0.5, 16, 0.5), CFrame.new(0, 8, z - dir * 30), Color3.fromRGB(80, 80, 80), M.Metal)
	P("Flag", Vector3.new(6, 4, 0.2), CFrame.new(3, 14, z - dir * 30), t.Color.Color, M.Fabric)
end

------------------------------------------------------------ ЯЩИКИ: ПАТРОНЫ И КОСТЮМЫ
local function crate(kind, x, z, label, outfitIdx)
	local color = kind == "ammo" and Color3.fromRGB(70, 86, 56) or Config.Outfits[outfitIdx].Shirt
	local p = P(kind == "ammo" and "AmmoCrate" or "OutfitCrate", Vector3.new(3, 2, 2), CFrame.new(x, 1, z), color, M.Metal)
	p:SetAttribute("Label", label)
	if outfitIdx then p:SetAttribute("Outfit", outfitIdx) end
	CS:AddTag(p, kind == "ammo" and "AmmoCrate" or "OutfitCrate")
	local bb = Instance.new("BillboardGui")
	bb.Size = UDim2.fromOffset(170, 24); bb.StudsOffset = Vector3.new(0, 2.2, 0); bb.MaxDistance = 60; bb.Adornee = p; bb.Parent = p
	local tl = Instance.new("TextLabel"); tl.Size = UDim2.fromScale(1, 1); tl.BackgroundTransparency = 1
	tl.Text = label; tl.Font = Enum.Font.GothamBold; tl.TextSize = 14; tl.TextColor3 = Color3.new(1, 1, 1)
	tl.TextStrokeTransparency = 0.4; tl.Parent = bb
end
for _, side in ipairs({-1, 1}) do
	crate("ammo", -70, side * 190, "Ящик с патронами")
	crate("ammo", 70, side * 190, "Ящик с патронами")
	crate("ammo", side * 130, 20 * side, "Ящик с патронами")
	for i, o in ipairs(Config.Outfits) do
		crate("outfit", -80 + (i - 1) * 40, side * 212, "Костюм: " .. o.Name, i)
	end
end
crate("ammo", 0, 0, "Ящик с патронами")

------------------------------------------------------------ ОСВЕЩЕНИЕ / АТМОСФЕРА
Lighting.ClockTime = 16.5
Lighting.Brightness = 1.6
Lighting.Ambient = Color3.fromRGB(70, 65, 60)
Lighting.OutdoorAmbient = Color3.fromRGB(95, 88, 80)
Lighting.FogColor = Color3.fromRGB(120, 105, 90)
Lighting.FogEnd = 900
local atm = Instance.new("Atmosphere")
atm.Density = 0.35; atm.Color = Color3.fromRGB(180, 150, 120); atm.Haze = 2.5; atm.Offset = 0.2; atm.Parent = Lighting
local cc = Instance.new("ColorCorrectionEffect")
cc.Saturation = -0.35; cc.Contrast = 0.15; cc.TintColor = Color3.fromRGB(255, 235, 215); cc.Parent = Lighting
```

---

## ЧАСТЬ 5. `ClientState` (ModuleScript в StarterPlayerScripts)

Общее хранилище настроек, клавиш и вспомогательных функций для двух клиентских скриптов.

```lua
local RS = game:GetService("ReplicatedStorage")
local Config = require(RS:WaitForChild("Config"))
local R = RS:WaitForChild("Remotes")

local State = {Data = nil, MenuOpen = false, Editing = false, Rebinding = false}
State.Changed = Instance.new("BindableEvent")
State.OpenMenu = Instance.new("BindableEvent")

local function copy(t)
	if type(t) ~= "table" then return t end
	local o = {}
	for k, v in pairs(t) do o[k] = copy(v) end
	return o
end
local function merge(dst, src)
	for k, v in pairs(src) do
		if type(v) == "table" and type(dst[k]) == "table" then merge(dst[k], v) else dst[k] = v end
	end
end

State.Settings = copy(Config.DefaultSettings)
State.Settings.Keys = copy(Config.DefaultKeys)

local PRETTY = {One = "1", Two = "2", Three = "3", Four = "4", MouseButton1 = "ЛКМ", MouseButton2 = "ПКМ",
	MouseButton3 = "СКМ", LeftShift = "Shift", LeftControl = "Ctrl", Space = "Пробел"}
function State.Pretty(n) return PRETTY[n] or n end

function State.InputName(input)
	if input.UserInputType == Enum.UserInputType.Keyboard then return input.KeyCode.Name end
	if input.UserInputType.Name:find("MouseButton") then return input.UserInputType.Name end
	return nil
end
function State.Matches(input, action)
	return State.InputName(input) == State.Settings.Keys[action]
end

local pending = false
function State.Save()
	State.Changed:Fire()
	if pending then return end
	pending = true
	task.delay(1, function()
		pending = false
		R.SaveSettings:FireServer(State.Settings)
	end)
end

function State.Refresh()
	local ok, d = pcall(function() return R.GetData:InvokeServer() end)
	if ok and d then
		State.Data = d
		if d.Settings then merge(State.Settings, d.Settings) end
		State.Changed:Fire()
	end
	return State.Data
end

task.spawn(function()
	repeat State.Refresh(); task.wait(1) until State.Data
end)

return State
```

---

## ЧАСТЬ 6. `GameClient` (LocalScript в StarterPlayerScripts)

HUD, стрельба, присед (C), зум (Z), перезарядка, слоты 1/2/3, килфид, индикатор «откуда стреляли», хитмаркер, FPV-дрон, мобильные кнопки с перетаскиванием.

```lua
local Players = game:GetService("Players")
local RS = game:GetService("ReplicatedStorage")
local UIS = game:GetService("UserInputService")
local RunService = game:GetService("RunService")
local TweenService = game:GetService("TweenService")
local GuiService = game:GetService("GuiService")
local Debris = game:GetService("Debris")
local SoundService = game:GetService("SoundService")
local TeamsService = game:GetService("Teams")

local plr = Players.LocalPlayer
local cam = workspace.CurrentCamera
local Config = require(RS:WaitForChild("Config"))
local State = require(script.Parent:WaitForChild("ClientState"))
local R = RS:WaitForChild("Remotes")

------------------------------------------------------------ UI helpers
local function new(class, props, parent)
	local o = Instance.new(class)
	for k, v in pairs(props) do o[k] = v end
	o.Parent = parent
	return o
end
local function label(props, parent)
	props.BackgroundTransparency = 1
	props.Font = props.Font or Enum.Font.GothamBold
	props.TextColor3 = props.TextColor3 or Color3.new(1, 1, 1)
	props.TextSize = props.TextSize or 18
	return new("TextLabel", props, parent)
end

local gui = new("ScreenGui", {Name = "HUD", ResetOnSpawn = false, IgnoreGuiInset = true, DisplayOrder = 5}, plr:WaitForChild("PlayerGui"))
local main = new("Frame", {Size = UDim2.fromScale(1, 1), BackgroundTransparency = 1, Visible = false}, gui)

------------------------------------------------------------ Прицел
local cross = {}
for _, k in ipairs({"top", "bot", "left", "right"}) do
	cross[k] = new("Frame", {BorderSizePixel = 0, AnchorPoint = Vector2.new(.5, .5)}, main)
end
local function updateCross()
	local s = State.Settings
	local c = Color3.fromRGB(s.CrosshairColor[1], s.CrosshairColor[2], s.CrosshairColor[3])
	local g, l = 6, s.CrosshairSize
	for _, f in pairs(cross) do f.BackgroundColor3 = c end
	cross.top.Size = UDim2.fromOffset(2, l);   cross.top.Position = UDim2.new(.5, 0, .5, -(g + l / 2))
	cross.bot.Size = UDim2.fromOffset(2, l);   cross.bot.Position = UDim2.new(.5, 0, .5, g + l / 2)
	cross.left.Size = UDim2.fromOffset(l, 2);  cross.left.Position = UDim2.new(.5, -(g + l / 2), .5, 0)
	cross.right.Size = UDim2.fromOffset(l, 2); cross.right.Position = UDim2.new(.5, g + l / 2, .5, 0)
end

-- оптический прицел (для сильного зума)
local scope = new("Frame", {Size = UDim2.fromScale(1, 1), BackgroundTransparency = 1, Visible = false}, main)
new("Frame", {Size = UDim2.new(1, 0, 0, 2), Position = UDim2.fromScale(0, .5), BackgroundColor3 = Color3.new(), BorderSizePixel = 0}, scope)
new("Frame", {Size = UDim2.new(0, 2, 1, 0), Position = UDim2.fromScale(.5, 0), BackgroundColor3 = Color3.new(), BorderSizePixel = 0}, scope)

------------------------------------------------------------ Здоровье / патроны / способность (низ по центру)
local ammoLbl = label({Size = UDim2.fromOffset(320, 34), AnchorPoint = Vector2.new(.5, 1), Position = UDim2.new(.5, 0, 1, -56), TextSize = 26}, main)
local weaponLbl = label({Size = UDim2.fromOffset(320, 20), AnchorPoint = Vector2.new(.5, 1), Position = UDim2.new(.5, 0, 1, -90), TextSize = 14, TextColor3 = Color3.fromRGB(200, 200, 190)}, main)
local abilityLbl = label({Size = UDim2.fromOffset(360, 22), AnchorPoint = Vector2.new(.5, 1), Position = UDim2.new(.5, 0, 1, -112), TextSize = 15, TextColor3 = Color3.fromRGB(255, 190, 80)}, main)
local hpBack = new("Frame", {Size = UDim2.fromOffset(260, 20), AnchorPoint = Vector2.new(.5, 1), Position = UDim2.new(.5, 0, 1, -28), BackgroundColor3 = Color3.fromRGB(20, 20, 20), BackgroundTransparency = .3, BorderSizePixel = 0}, main)
local hpFill = new("Frame", {Size = UDim2.fromScale(1, 1), BackgroundColor3 = Color3.fromRGB(90, 200, 90), BorderSizePixel = 0}, hpBack)
local hpText = label({Size = UDim2.fromScale(1, 1), TextSize = 14}, hpBack)

------------------------------------------------------------ Счёт команд, килфид, уведомления
local scoreA = label({Size = UDim2.fromOffset(120, 36), AnchorPoint = Vector2.new(1, 0), Position = UDim2.new(.5, -10, 0, 12), TextSize = 30, TextXAlignment = Enum.TextXAlignment.Right}, gui)
local scoreB = label({Size = UDim2.fromOffset(120, 36), Position = UDim2.new(.5, 10, 0, 12), TextSize = 30, TextXAlignment = Enum.TextXAlignment.Left}, gui)
label({Size = UDim2.fromOffset(20, 36), AnchorPoint = Vector2.new(.5, 0), Position = UDim2.new(.5, 0, 0, 12), Text = ":", TextSize = 30}, gui)

local feed = new("Frame", {Size = UDim2.fromOffset(420, 220), AnchorPoint = Vector2.new(1, 0), Position = UDim2.new(1, -16, 0, 60), BackgroundTransparency = 1}, gui)
new("UIListLayout", {Padding = UDim.new(0, 4), HorizontalAlignment = Enum.HorizontalAlignment.Right, VerticalAlignment = Enum.VerticalAlignment.Top, SortOrder = Enum.SortOrder.LayoutOrder}, feed)

local noteLbl = label({Size = UDim2.fromOffset(600, 30), AnchorPoint = Vector2.new(.5, 0), Position = UDim2.new(.5, 0, 0, 64), TextSize = 22, TextTransparency = 1, TextStrokeTransparency = 1}, gui)
local noteId = 0
local function notify(text, color)
	noteId += 1; local id = noteId
	noteLbl.Text = text; noteLbl.TextColor3 = color or Color3.fromRGB(255, 200, 80)
	noteLbl.TextTransparency = 0; noteLbl.TextStrokeTransparency = 0.5
	task.delay(3.5, function()
		if noteId == id then TweenService:Create(noteLbl, TweenInfo.new(.5), {TextTransparency = 1, TextStrokeTransparency = 1}):Play() end
	end)
end
R.Notify.OnClientEvent:Connect(notify)

local hit = label({Size = UDim2.fromOffset(40, 40), AnchorPoint = Vector2.new(.5, .5), Position = UDim2.fromScale(.5, .5), Text = "✕", TextSize = 34, TextTransparency = 1}, gui)

local function hex(c) return "#" .. c:ToHex() end
local feedOrder = 0
R.KillFeed.OnClientEvent:Connect(function(k, kc, v, vc, weapon, head)
	local txt
	if k == "" then
		txt = string.format('<font color="%s">%s</font> погиб', hex(vc), v)
	else
		txt = string.format('<font color="%s">%s</font>  [%s]%s  <font color="%s">%s</font>', hex(kc), k, weapon, head and " ⌖" or "", hex(vc), v)
	end
	feedOrder += 1
	local mine = (k == plr.Name)
	local e = new("TextLabel", {Size = UDim2.fromOffset(0, 24), AutomaticSize = Enum.AutomaticSize.X, RichText = true, Text = "  " .. txt .. "  ",
		TextSize = 16, Font = Enum.Font.GothamBold, TextColor3 = Color3.new(1, 1, 1), BackgroundColor3 = mine and Color3.fromRGB(150, 90, 20) or Color3.new(),
		BackgroundTransparency = .45, BorderSizePixel = 0, LayoutOrder = feedOrder}, feed)
	Debris:AddItem(e, 6)
	if v == plr.Name and k ~= "" then notify("Вас убил " .. k .. " (" .. weapon .. ")", Color3.fromRGB(255, 90, 90)) end
end)

------------------------------------------------------------ Хитмаркер, трассеры, индикатор урона
R.HitMark.OnClientEvent:Connect(function(head, kill)
	if not State.Settings.Hitmarker then return end
	hit.TextColor3 = kill and Color3.fromRGB(255, 60, 60) or Color3.new(1, 1, 1)
	hit.TextTransparency = 0
	TweenService:Create(hit, TweenInfo.new(.25), {TextTransparency = 1}):Play()
	local id = (kill and Config.Sounds.Kill ~= "") and Config.Sounds.Kill or Config.Sounds.Hit
	if id ~= "" then
		local s = Instance.new("Sound"); s.SoundId = id; s.Parent = SoundService; s:Play(); Debris:AddItem(s, 2)
	end
end)

R.Tracer.OnClientEvent:Connect(function(from, to)
	local d = (to - from).Magnitude; if d < 1 then return end
	local p = Instance.new("Part")
	p.Anchored = true; p.CanCollide = false; p.CanQuery = false; p.CanTouch = false
	p.Material = Enum.Material.Neon; p.Color = Color3.fromRGB(255, 220, 120)
	p.Size = Vector3.new(.06, .06, d); p.CFrame = CFrame.lookAt(from, to) * CFrame.new(0, 0, -d / 2)
	p.Parent = workspace:FindFirstChild("Effects") or workspace
	TweenService:Create(p, TweenInfo.new(.15), {Transparency = 1}):Play()
	if Config.Sounds.Shot ~= "" then
		local s = Instance.new("Sound"); s.SoundId = Config.Sounds.Shot; s.RollOffMaxDistance = 200; s.Parent = p; s:Play()
		Debris:AddItem(p, 1.5)
	else
		Debris:AddItem(p, .2)
	end
end)

local inds = {}
R.Damaged.OnClientEvent:Connect(function(pos)
	local holder = new("Frame", {Size = UDim2.fromOffset(320, 320), AnchorPoint = Vector2.new(.5, .5), Position = UDim2.fromScale(.5, .5), BackgroundTransparency = 1}, gui)
	local arrow = label({Size = UDim2.fromOffset(60, 40), AnchorPoint = Vector2.new(.5, 0), Position = UDim2.fromScale(.5, 0), Text = "▲", TextSize = 36, TextColor3 = Color3.fromRGB(230, 40, 40)}, holder)
	table.insert(inds, {holder = holder, arrow = arrow, pos = pos, t = os.clock()})
end)

------------------------------------------------------------ Состояние управления
local fireHeld, fireLatch, lastShot = false, false, 0
local crouch, zoomIdx, recoil = false, 0, 0
local piloting, upUntil, savedJump = nil, 0, nil
local mobileDevice = UIS.TouchEnabled and not UIS.KeyboardEnabled

local droneLbl = label({Size = UDim2.fromOffset(500, 30), AnchorPoint = Vector2.new(.5, 0), Position = UDim2.new(.5, 0, 0, 110), TextSize = 20, TextColor3 = Color3.fromRGB(255, 80, 80), Visible = false,
	Text = "ДРОН: WASD — полёт, Пробел/C — вверх/вниз, [3] — подрыв"}, gui)

local function zoomList()
	local w = Config.Weapons[plr:GetAttribute("Weapon")]
	return w and w.Zoom or {1.4}
end

local function press(action, down)
	if State.MenuOpen or State.Rebinding then if action == "Fire" and not down then fireHeld = false end return end
	if action == "Fire" then
		fireHeld = down
		if down then fireLatch = true end
	elseif action == "Crouch" then
		if mobileDevice then if down then crouch = not crouch end else crouch = down end
	elseif not down then
		return
	elseif action == "Reload" then
		R.Reload:FireServer()
	elseif action == "Slot1" or action == "Slot2" then
		zoomIdx = 0; R.Equip:FireServer(action == "Slot1" and 1 or 2)
	elseif action == "Ability" then
		if piloting then R.DroneDetonate:FireServer() else R.Ability:FireServer() end
	elseif action == "Zoom" then
		zoomIdx += 1
		if zoomIdx > #zoomList() then zoomIdx = 0 end
	end
end

UIS.InputBegan:Connect(function(i, gp)
	if gp then return end
	local n = State.InputName(i); if not n then return end
	for action, key in pairs(State.Settings.Keys) do
		if key == n then press(action, true) end
	end
end)
UIS.InputEnded:Connect(function(i)
	local n = State.InputName(i); if not n then return end
	for action, key in pairs(State.Settings.Keys) do
		if key == n and (action == "Fire" or action == "Crouch") then press(action, false) end
	end
end)
UIS.JumpRequest:Connect(function() upUntil = os.clock() + .15 end)

------------------------------------------------------------ Мобильные кнопки (настраиваемые)
local MOB = {
	Fire    = {x = .80, y = .55, s = 92, t = "ОГОНЬ"},
	Zoom    = {x = .90, y = .38, s = 64, t = "ЗУМ"},
	Reload  = {x = .70, y = .72, s = 64, t = "R"},
	Crouch  = {x = .60, y = .84, s = 64, t = "ПРИС"},
	Slot1   = {x = .60, y = .14, s = 56, t = "1"},
	Slot2   = {x = .68, y = .14, s = 56, t = "2"},
	Ability = {x = .76, y = .14, s = 56, t = "3"},
}
local mobFrame = new("Frame", {Size = UDim2.fromScale(1, 1), BackgroundTransparency = 1, Visible = false}, gui)
local mobBtns = {}

local function layoutMobile()
	local s = State.Settings
	for name, b in pairs(mobBtns) do
		local d = MOB[name]; local p = s.MobilePos[name]
		local sz = d.s * s.MobileScale
		b.Size = UDim2.fromOffset(sz, sz)
		b.Position = UDim2.fromScale(p and p[1] or d.x, p and p[2] or d.y)
		b.BackgroundTransparency = 1 - s.MobileOpacity
	end
end

local drag
for name, d in pairs(MOB) do
	local b = new("TextButton", {AnchorPoint = Vector2.new(.5, .5), Text = d.t, Font = Enum.Font.GothamBold, TextSize = 16, TextColor3 = Color3.new(1, 1, 1),
		BackgroundColor3 = Color3.fromRGB(30, 30, 30), AutoButtonColor = false, BorderSizePixel = 0}, mobFrame)
	new("UICorner", {CornerRadius = UDim.new(1, 0)}, b)
	new("UIStroke", {Color = Color3.fromRGB(230, 150, 40), Thickness = 2}, b)
	mobBtns[name] = b
	b.InputBegan:Connect(function(i)
		if i.UserInputType ~= Enum.UserInputType.Touch and i.UserInputType ~= Enum.UserInputType.MouseButton1 then return end
		if State.Editing then drag = {name = name, b = b}; return end
		press(name, true)
	end)
	b.InputEnded:Connect(function(i)
		if i.UserInputType ~= Enum.UserInputType.Touch and i.UserInputType ~= Enum.UserInputType.MouseButton1 then return end
		if not State.Editing then press(name, false) end
	end)
end

UIS.InputChanged:Connect(function(i)
	if not drag then return end
	if i.UserInputType == Enum.UserInputType.Touch or i.UserInputType == Enum.UserInputType.MouseMovement then
		local inset = GuiService:GetGuiInset()
		local vs = gui.AbsoluteSize
		local x = math.clamp((i.Position.X + inset.X) / vs.X, .03, .97)
		local y = math.clamp((i.Position.Y + inset.Y) / vs.Y, .05, .95)
		drag.b.Position = UDim2.fromScale(x, y)
		State.Settings.MobilePos[drag.name] = {x, y}
	end
end)
UIS.InputEnded:Connect(function(i)
	if drag and (i.UserInputType == Enum.UserInputType.Touch or i.UserInputType == Enum.UserInputType.MouseButton1) then
		drag = nil; State.Save()
	end
end)

local editBar = new("TextButton", {Size = UDim2.fromOffset(340, 44), AnchorPoint = Vector2.new(.5, 0), Position = UDim2.new(.5, 0, 0, 20),
	Text = "ГОТОВО — сохранить расположение кнопок", Font = Enum.Font.GothamBold, TextSize = 16, TextColor3 = Color3.new(),
	BackgroundColor3 = Color3.fromRGB(230, 150, 40), Visible = false, BorderSizePixel = 0}, gui)
editBar.Activated:Connect(function()
	State.Editing = false; State.Save(); State.OpenMenu:Fire()
end)

------------------------------------------------------------ Дрон
R.DroneStart.OnClientEvent:Connect(function(drone)
	local hum = plr.Character and plr.Character:FindFirstChildOfClass("Humanoid")
	if not hum then return end
	piloting = drone; fireHeld = false
	savedJump = {hum.JumpPower, hum.JumpHeight}
	hum.JumpPower = 0; hum.JumpHeight = 0
	cam.CameraSubject = drone
	droneLbl.Visible = true
end)
R.DroneEnd.OnClientEvent:Connect(function()
	piloting = nil; droneLbl.Visible = false
	local hum = plr.Character and plr.Character:FindFirstChildOfClass("Humanoid")
	if hum then
		cam.CameraSubject = hum
		if savedJump then hum.JumpPower = savedJump[1]; hum.JumpHeight = savedJump[2] end
	end
end)

------------------------------------------------------------ Главный цикл
local function applyCamMode()
	plr.CameraMode = State.Settings.FirstPerson and Enum.CameraMode.LockFirstPerson or Enum.CameraMode.Classic
	plr.CameraMaxZoomDistance = State.Settings.FirstPerson and 0.5 or 10
end
State.Changed.Event:Connect(function() updateCross(); layoutMobile(); applyCamMode() end)
updateCross(); layoutMobile(); applyCamMode()

local function pretty(a) return State.Pretty(State.Settings.Keys[a]) end

RunService:BindToRenderStep("FrontlineMain", Enum.RenderPriority.Camera.Value + 1, function(dt)
	gui.Enabled = not State.MenuOpen
	local char = plr.Character
	local hum = char and char:FindFirstChildOfClass("Humanoid")
	local alive = hum ~= nil and hum.Health > 0
	main.Visible = alive
	mobFrame.Visible = UIS.TouchEnabled and (alive or State.Editing)
	editBar.Visible = State.Editing

	-- счёт команд
	local tA, tB = TeamsService:FindFirstChild(Config.Teams[1].Name), TeamsService:FindFirstChild(Config.Teams[2].Name)
	if tA and tB then
		scoreA.Text = tostring(tA:GetAttribute("Score") or 0); scoreA.TextColor3 = tA.TeamColor.Color
		scoreB.Text = tostring(tB:GetAttribute("Score") or 0); scoreB.TextColor3 = tB.TeamColor.Color
	end

	-- индикаторы урона
	for i = #inds, 1, -1 do
		local d = inds[i]; local age = os.clock() - d.t
		if age > 1.6 then d.holder:Destroy(); table.remove(inds, i)
		else
			local rel = cam.CFrame:PointToObjectSpace(d.pos)
			d.holder.Rotation = math.deg(math.atan2(rel.X, -rel.Z))
			d.arrow.TextTransparency = age / 1.6
		end
	end

	if not alive then
		UIS.MouseDeltaSensitivity = 1
		zoomIdx = 0; crouch = false
		return
	end

	-- HUD
	local wname = plr:GetAttribute("Weapon") or "-"
	local cfg = Config.Weapons[wname]
	ammoLbl.Text = plr:GetAttribute("Reloading") and "ПЕРЕЗАРЯДКА..." or string.format("%d / %d", plr:GetAttribute("Mag") or 0, plr:GetAttribute("Reserve") or 0)
	weaponLbl.Text = string.format("[%s] %s", (plr:GetAttribute("Slot") or 1) == 1 and pretty("Slot1") or pretty("Slot2"), wname)
	local ready = (plr:GetAttribute("AbilityReadyAt") or 0) - workspace:GetServerTimeNow()
	abilityLbl.Text = string.format("[%s] %s  %s", pretty("Ability"), plr:GetAttribute("AbilityName") or "", ready > 0 and (math.ceil(ready) .. "с") or "ГОТОВО")
	local hp = math.clamp(hum.Health / hum.MaxHealth, 0, 1)
	hpFill.Size = UDim2.fromScale(hp, 1); hpText.Text = tostring(math.ceil(hum.Health))
	hpFill.BackgroundColor3 = Color3.fromRGB(220 * (1 - hp) + 40, 200 * hp + 30, 40)

	-- скорость / присед
	local base = char:GetAttribute("BaseSpeed") or 16
	hum.WalkSpeed = piloting and 0 or base * (crouch and .55 or 1) * (zoomIdx > 0 and .8 or 1)
	hum.CameraOffset = hum.CameraOffset:Lerp(Vector3.new(0, crouch and -1.5 or 0, 0), math.min(1, dt * 10))

	-- зум
	local zl = (zoomIdx > 0 and not piloting) and (zoomList()[zoomIdx] or 1.4) or 1
	cam.FieldOfView += (State.Settings.FOV / zl - cam.FieldOfView) * math.min(1, dt * 12)
	UIS.MouseDeltaSensitivity = 1 / zl
	scope.Visible = zl >= 3
	for _, f in pairs(cross) do f.Visible = zl < 3 end

	-- отдача (визуальная)
	if recoil > 0.01 then
		cam.CFrame = cam.CFrame * CFrame.Angles(math.rad(recoil), 0, 0)
		recoil -= recoil * math.min(1, dt * 10)
	end

	-- стрельба
	if fireHeld and cfg and not piloting and not State.MenuOpen then
		local now = os.clock()
		local mag = plr:GetAttribute("Mag") or 0
		if mag <= 0 then
			if not plr:GetAttribute("Reloading") then R.Reload:FireServer() end
		elseif not plr:GetAttribute("Reloading") and now - lastShot >= 60 / cfg.RPM and (cfg.Auto or fireLatch) then
			lastShot = now; fireLatch = false
			R.Fire:FireServer(cam.CFrame.Position, cam.CFrame.LookVector)
			recoil += cfg.Recoil
		end
	end

	-- управление дроном
	if piloting then
		if not piloting.Parent then
			piloting = nil; droneLbl.Visible = false; cam.CameraSubject = hum
		else
			local bv = piloting:FindFirstChildOfClass("BodyVelocity")
			if bv then
				local speed = 70
				local vel = hum.MoveDirection * speed
				local look = cam.CFrame.LookVector
				local flat = Vector3.new(look.X, 0, look.Z)
				if flat.Magnitude > .01 then
					local f = hum.MoveDirection:Dot(flat.Unit)
					vel += Vector3.new(0, math.clamp(look.Y / flat.Magnitude, -3, 3) * f * speed, 0)
				end
				if UIS:IsKeyDown(Enum.KeyCode.Space) or os.clock() < upUntil then vel += Vector3.new(0, 45, 0) end
				if UIS:IsKeyDown(Enum.KeyCode[State.Settings.Keys.Crouch] or Enum.KeyCode.C) then vel -= Vector3.new(0, 45, 0) end
				bv.Velocity = vel
			end
		end
	end
end)

plr.CharacterAdded:Connect(function()
	crouch = false; zoomIdx = 0; piloting = nil; droneLbl.Visible = false; applyCamMode()
end)
```

> Примечание: в `Enum.KeyCode[State.Settings.Keys.Crouch]` используется имя клавиши. Если игрок назначил на присед кнопку мыши, дрон будет снижаться по умолчанию на клавише C.

---

## ЧАСТЬ 7. `MenuClient` (LocalScript в StarterPlayerScripts)

Главное меню в стиле «военный штаб»: В БОЙ, Роли, Оружие, Магазин, Кредиты (донат), VIP, Поддержать, Настройки (клавиши ПК, прицел, FOV, мобильные кнопки).

```lua
local Players = game:GetService("Players")
local RS = game:GetService("ReplicatedStorage")
local UIS = game:GetService("UserInputService")
local MPS = game:GetService("MarketplaceService")

local plr = Players.LocalPlayer
local Config = require(RS:WaitForChild("Config"))
local State = require(script.Parent:WaitForChild("ClientState"))
local R = RS:WaitForChild("Remotes")

local BG, PANEL, ACC = Color3.fromRGB(20, 23, 18), Color3.fromRGB(32, 37, 28), Color3.fromRGB(226, 150, 40)
local TXT, DIM = Color3.fromRGB(230, 226, 214), Color3.fromRGB(150, 150, 140)

local function new(class, props, parent)
	local o = Instance.new(class)
	for k, v in pairs(props) do o[k] = v end
	o.Parent = parent
	return o
end
local function label(props, parent)
	props.BackgroundTransparency = 1
	props.Font = props.Font or Enum.Font.GothamBold
	props.TextColor3 = props.TextColor3 or TXT
	props.TextSize = props.TextSize or 18
	props.TextXAlignment = props.TextXAlignment or Enum.TextXAlignment.Left
	return new("TextLabel", props, parent)
end
local function button(props, parent, cb)
	props.Font = props.Font or Enum.Font.GothamBold
	props.TextSize = props.TextSize or 18
	props.TextColor3 = props.TextColor3 or TXT
	props.BackgroundColor3 = props.BackgroundColor3 or PANEL
	props.BorderSizePixel = 0
	local b = new("TextButton", props, parent)
	new("UICorner", {CornerRadius = UDim.new(0, 4)}, b)
	if cb then b.Activated:Connect(cb) end
	return b
end

------------------------------------------------------------ Каркас
local gui = new("ScreenGui", {Name = "Menu", ResetOnSpawn = false, IgnoreGuiInset = true, DisplayOrder = 50}, plr:WaitForChild("PlayerGui"))
local root = new("Frame", {Size = UDim2.fromScale(1, 1), BackgroundColor3 = BG, BackgroundTransparency = .05, BorderSizePixel = 0}, gui)
new("TextButton", {Size = UDim2.fromOffset(0, 0), Text = "", Modal = true, BackgroundTransparency = 1}, root) -- освобождает мышь в режиме от первого лица

label({Position = UDim2.fromOffset(40, 24), Size = UDim2.fromOffset(500, 50), Text = "ФРОНТЛАЙН", TextSize = 46, TextColor3 = ACC}, root)
label({Position = UDim2.fromOffset(42, 74), Size = UDim2.fromOffset(500, 24), Text = "П Е П Е Л   •   ТАКТИЧЕСКИЙ ШУТЕР", TextSize = 14, TextColor3 = DIM}, root)
local creditsLbl = label({AnchorPoint = Vector2.new(1, 0), Position = UDim2.new(1, -40, 0, 36), Size = UDim2.fromOffset(300, 30), Text = "", TextSize = 22, TextXAlignment = Enum.TextXAlignment.Right}, root)

local nav = new("Frame", {Position = UDim2.fromOffset(40, 120), Size = UDim2.fromOffset(240, 520), BackgroundTransparency = 1}, root)
new("UIListLayout", {Padding = UDim.new(0, 8)}, nav)

local content = new("ScrollingFrame", {Position = UDim2.fromOffset(310, 110), Size = UDim2.new(1, -350, 1, -140), BackgroundColor3 = PANEL, BorderSizePixel = 0,
	ScrollBarThickness = 6, AutomaticCanvasSize = Enum.AutomaticSize.Y, CanvasSize = UDim2.new()}, root)
new("UIListLayout", {Padding = UDim.new(0, 8), SortOrder = Enum.SortOrder.LayoutOrder}, content)
new("UIPadding", {PaddingTop = UDim.new(0, 12), PaddingLeft = UDim.new(0, 14), PaddingRight = UDim.new(0, 14), PaddingBottom = UDim.new(0, 14)}, content)

local conns, order = {}, 0
local function track(c) conns[#conns + 1] = c; return c end
local function nextOrder() order += 1; return order end
local function clear()
	for _, c in ipairs(conns) do c:Disconnect() end
	table.clear(conns); order = 0
	for _, ch in ipairs(content:GetChildren()) do
		if not ch:IsA("UIListLayout") and not ch:IsA("UIPadding") then ch:Destroy() end
	end
end

local function header(text)
	return label({Size = UDim2.new(1, 0, 0, 30), Text = text, TextSize = 22, TextColor3 = ACC, LayoutOrder = nextOrder()}, content)
end
local function text(str, h, color)
	return label({Size = UDim2.new(1, 0, 0, h or 24), Text = str, TextWrapped = true, TextSize = 16, TextColor3 = color or TXT, RichText = true, LayoutOrder = nextOrder(), TextYAlignment = Enum.TextYAlignment.Top}, content)
end
local function card(h)
	local f = new("Frame", {Size = UDim2.new(1, 0, 0, h), BackgroundColor3 = BG, BorderSizePixel = 0, LayoutOrder = nextOrder()}, content)
	new("UICorner", {CornerRadius = UDim.new(0, 4)}, f)
	return f
end
local function bigButton(txt, cb, color)
	return button({Size = UDim2.new(1, 0, 0, 44), Text = txt, BackgroundColor3 = color or ACC, TextColor3 = color and TXT or Color3.new(), LayoutOrder = nextOrder()}, content, cb)
end

local function slider(textStr, min, max, value, cb)
	local row = new("Frame", {Size = UDim2.new(1, 0, 0, 46), BackgroundTransparency = 1, LayoutOrder = nextOrder()}, content)
	local lbl = label({Size = UDim2.new(1, 0, 0, 20), Text = textStr .. ": " .. value, TextSize = 15}, row)
	local track_ = new("Frame", {Size = UDim2.new(1, 0, 0, 16), Position = UDim2.fromOffset(0, 26), BackgroundColor3 = BG, BorderSizePixel = 0}, row)
	local fill = new("Frame", {Size = UDim2.fromScale((value - min) / (max - min), 1), BackgroundColor3 = ACC, BorderSizePixel = 0}, track_)
	local dragging = false
	local function setX(x)
		local a = math.clamp((x - track_.AbsolutePosition.X) / track_.AbsoluteSize.X, 0, 1)
		local v = math.floor((min + (max - min) * a) * 100 + .5) / 100
		fill.Size = UDim2.fromScale(a, 1); lbl.Text = textStr .. ": " .. v; cb(v)
	end
	track(track_.InputBegan:Connect(function(i)
		if i.UserInputType == Enum.UserInputType.MouseButton1 or i.UserInputType == Enum.UserInputType.Touch then dragging = true; setX(i.Position.X) end
	end))
	track(UIS.InputChanged:Connect(function(i)
		if dragging and (i.UserInputType == Enum.UserInputType.MouseMovement or i.UserInputType == Enum.UserInputType.Touch) then setX(i.Position.X) end
	end))
	track(UIS.InputEnded:Connect(function(i)
		if dragging and (i.UserInputType == Enum.UserInputType.MouseButton1 or i.UserInputType == Enum.UserInputType.Touch) then dragging = false; State.Save() end
	end))
end

local function toggle(textStr, value, cb)
	local b
	b = button({Size = UDim2.new(1, 0, 0, 38), Text = "", LayoutOrder = nextOrder(), BackgroundColor3 = BG}, content, function()
		value = not value; cb(value); b.Text = textStr .. ":  " .. (value and "ВКЛ" or "ВЫКЛ"); State.Save()
	end)
	b.Text = textStr .. ":  " .. (value and "ВКЛ" or "ВЫКЛ")
end

------------------------------------------------------------ Открыть/закрыть
local pages, current = {}, "home"
local function show(name)
	current = name
	clear()
	pages[name]()
end
local function setOpen(v)
	root.Visible = v; State.MenuOpen = v
	if v then State.Refresh(); show(current) end
end
local function refreshCredits()
	local d = State.Data
	creditsLbl.Text = d and ("КРЕДИТЫ: " .. d.Credits .. (d.VIP and "   ★ VIP" or "")) or ""
end
State.Changed.Event:Connect(refreshCredits)
State.OpenMenu.Event:Connect(function() setOpen(true) end)

------------------------------------------------------------ Страницы
local function timeLeft(s)
	return string.format("%dд %dч", math.floor(s / 86400), math.floor(s % 86400 / 3600))
end

function pages.home()
	local d = State.Data
	header("ШТАБ")
	if not d then text("Загрузка данных...") return end
	local role = Config.Roles[d.Role]
	text(string.format("Роль: <b>%s</b> — способность: %s", role.Title, Config.Abilities[role.Ability].Title), 24)
	text(string.format("Основное: <b>%s</b>   Запасное: <b>%s</b>", d.Slot1, d.Slot2), 24)
	local c = card(90)
	label({Position = UDim2.fromOffset(14, 8), Size = UDim2.new(1, -28, 0, 26), Text = "★ АКЦИЯ НЕДЕЛИ: " .. d.Deal.Title, TextSize = 22, TextColor3 = ACC}, c)
	local lines = {}
	for n, p in pairs(d.Deal.Discounts) do table.insert(lines, string.format("%s -%d%%", n, p * 100)) end
	if d.Deal.CreditMult > 1 then table.insert(lines, "кредиты за убийства x" .. d.Deal.CreditMult) end
	label({Position = UDim2.fromOffset(14, 38), Size = UDim2.new(1, -28, 0, 40), Text = table.concat(lines, "  •  ") .. "\nДо конца акции: " .. timeLeft(d.TimeLeft), TextSize = 15, TextWrapped = true}, c)
	text("Управление (ПК): ЛКМ — огонь, C — присед, 1/2 — оружие, 3 — способность, Z — зум, R — перезарядка, E — подобрать ящик, M — меню.", 48, DIM)
	bigButton("В БОЙ", function()
		R.Deploy:FireServer(); setOpen(false)
	end)
end

function pages.roles()
	header("РОЛИ")
	local d = State.Data; if not d then return end
	for _, key in ipairs(Config.RoleOrder) do
		local r = Config.Roles[key]
		local c = card(92)
		label({Position = UDim2.fromOffset(14, 8), Size = UDim2.new(1, -170, 0, 26), Text = r.Title, TextSize = 22, TextColor3 = ACC}, c)
		label({Position = UDim2.fromOffset(14, 36), Size = UDim2.new(1, -170, 0, 50), Text = string.format("%s\nЗдоровье %d  •  Скорость %d  •  [3] %s", r.Desc, r.Health, r.Speed, Config.Abilities[r.Ability].Title), TextSize = 14, TextWrapped = true, TextColor3 = DIM, TextYAlignment = Enum.TextYAlignment.Top}, c)
		button({AnchorPoint = Vector2.new(1, .5), Position = UDim2.new(1, -12, .5, 0), Size = UDim2.fromOffset(130, 40), Text = d.Role == key and "ВЫБРАНО" or "ВЫБРАТЬ",
			BackgroundColor3 = d.Role == key and Color3.fromRGB(70, 110, 60) or ACC, TextColor3 = d.Role == key and TXT or Color3.new()}, c, function()
			R.SetRole:FireServer(key); d.Role = key; show("roles")
		end)
	end
end

local function sortedWeapons(slot)
	local list = {}
	for n, w in pairs(Config.Weapons) do if w.Slot == slot then table.insert(list, n) end end
	table.sort(list, function(a, b)
		local wa, wb = Config.Weapons[a], Config.Weapons[b]
		if wa.Price ~= wb.Price then return wa.Price < wb.Price end
		return a < b
	end)
	return list
end
local function stats(w)
	return string.format("%s  •  Урон %d  •  %d выстр/мин  •  Магазин %d", w.Type, w.Damage * w.Pellets, w.RPM, w.Mag)
end

function pages.loadout()
	header("ЭКИПИРОВКА")
	local d = State.Data; if not d then return end
	for slot = 1, 2 do
		text(slot == 1 and "ОСНОВНОЕ ОРУЖИЕ (клавиша 1)" or "ЗАПАСНОЕ ОРУЖИЕ (клавиша 2)", 24, ACC)
		for _, n in ipairs(sortedWeapons(slot)) do
			local w = Config.Weapons[n]; local c = card(64)
			label({Position = UDim2.fromOffset(14, 6), Size = UDim2.new(1, -170, 0, 24), Text = n, TextSize = 20}, c)
			label({Position = UDim2.fromOffset(14, 32), Size = UDim2.new(1, -170, 0, 24), Text = stats(w), TextSize = 13, TextColor3 = DIM}, c)
			local owned = d.Owned[n]; local sel = d["Slot" .. slot] == n
			button({AnchorPoint = Vector2.new(1, .5), Position = UDim2.new(1, -12, .5, 0), Size = UDim2.fromOffset(130, 38),
				Text = sel and "ВЫБРАНО" or (owned and "ВЫБРАТЬ" or (w.VIPOnly and "★ VIP" or "🔒 В магазине")),
				BackgroundColor3 = sel and Color3.fromRGB(70, 110, 60) or (owned and ACC or Color3.fromRGB(60, 60, 56)),
				TextColor3 = (owned and not sel) and Color3.new() or TXT}, c, function()
				if not owned then return end
				R.SetLoadout:FireServer(slot, n); d["Slot" .. slot] = n; show("loadout")
			end)
		end
	end
end

function pages.shop()
	header("МАГАЗИН (за кредиты)")
	local d = State.Data; if not d then return end
	text("★ Акция недели: " .. d.Deal.Title .. " — до конца " .. timeLeft(d.TimeLeft), 24, ACC)
	local list = {}
	for n, w in pairs(Config.Weapons) do if w.Price > 0 or w.VIPOnly then table.insert(list, n) end end
	table.sort(list)
	for _, n in ipairs(list) do
		local w = Config.Weapons[n]; local c = card(70)
		label({Position = UDim2.fromOffset(14, 6), Size = UDim2.new(1, -190, 0, 24), Text = n .. (d.Deal.Discounts[n] and string.format("   <font color='#e29628'>-%d%%</font>", d.Deal.Discounts[n] * 100) or ""), RichText = true, TextSize = 20}, c)
		label({Position = UDim2.fromOffset(14, 34), Size = UDim2.new(1, -190, 0, 24), Text = stats(w), TextSize = 13, TextColor3 = DIM}, c)
		local owned = d.Owned[n]
		local txt = owned and "КУПЛЕНО" or (w.VIPOnly and "★ ТОЛЬКО VIP" or ("КУПИТЬ " .. d.Prices[n]))
		button({AnchorPoint = Vector2.new(1, .5), Position = UDim2.new(1, -12, .5, 0), Size = UDim2.fromOffset(150, 40), Text = txt,
			BackgroundColor3 = owned and Color3.fromRGB(70, 110, 60) or ACC, TextColor3 = owned and TXT or Color3.new()}, c, function()
			if owned or w.VIPOnly then return end
			local ok, msg = R.Buy:InvokeServer(n)
			State.Refresh(); refreshCredits(); show("shop")
			text(msg, 24, ok and Color3.fromRGB(120, 255, 120) or Color3.fromRGB(255, 100, 100))
		end)
	end
end

local function productButton(txt, id)
	bigButton(txt, function()
		if id == 0 then text("Продукт ещё не настроен (вставьте ID в Config)", 24, Color3.fromRGB(255, 120, 120)) return end
		MPS:PromptProductPurchase(plr, id)
	end, PANEL)
end

function pages.credits()
	header("КРЕДИТЫ")
	text("Пополните кредиты за Robux — тратьте на оружие в магазине.", 24, DIM)
	for _, p in ipairs(Config.Products.Credits) do productButton(string.format("%d кредитов — %d R$", p.Amount, p.Robux), p.Id) end
end

function pages.vip()
	header("★ VIP-ПРОПУСК")
	local d = State.Data
	text("• Кредиты за убийства x2\n• Скидка 20% в магазине\n• Эксклюзивная винтовка «Фантом-VIP» (золотая)\n• Метка [VIP] над персонажем", 100)
	if d and d.VIP then text("У вас уже есть VIP. Спасибо!", 30, ACC)
	else
		bigButton("КУПИТЬ VIP", function()
			if Config.VIPGamePassId == 0 then text("VIP ещё не настроен (вставьте ID в Config)", 24, Color3.fromRGB(255, 120, 120)) return end
			MPS:PromptGamePassPurchase(plr, Config.VIPGamePassId)
		end)
	end
end

function pages.support()
	header("ПОДДЕРЖАТЬ АВТОРА")
	text("Игра делается одним человеком. Любая поддержка помогает выпускать обновления. В благодарность вы получите бонусные кредиты и метку «Supporter».", 70, DIM)
	for _, p in ipairs(Config.Products.Support) do productButton(string.format("Поддержать на %d R$", p.Robux), p.Id) end
end

local ACTIONS = {{"Fire", "Стрельба"}, {"Crouch", "Присесть"}, {"Reload", "Перезарядка"}, {"Slot1", "Оружие 1"},
	{"Slot2", "Оружие 2"}, {"Ability", "Способность"}, {"Zoom", "Зум"}, {"Menu", "Меню"}}

function pages.settings()
	local S = State.Settings
	header("УПРАВЛЕНИЕ (ПК) — нажмите на кнопку и затем на новую клавишу")
	for _, a in ipairs(ACTIONS) do
		local action = a[1]
		local row = new("Frame", {Size = UDim2.new(1, 0, 0, 38), BackgroundTransparency = 1, LayoutOrder = nextOrder()}, content)
		label({Size = UDim2.new(1, -170, 1, 0), Text = a[2], TextSize = 16}, row)
		local b
		b = button({AnchorPoint = Vector2.new(1, .5), Position = UDim2.new(1, 0, .5, 0), Size = UDim2.fromOffset(150, 32), Text = State.Pretty(S.Keys[action]), BackgroundColor3 = BG}, row, function()
			if State.Rebinding then return end
			State.Rebinding = true; b.Text = "..."
			local c
			c = UIS.InputBegan:Connect(function(i)
				local n = State.InputName(i); if not n then return end
				c:Disconnect(); State.Rebinding = false
				if n ~= "Escape" then
					for k, v in pairs(S.Keys) do if v == n and k ~= action then S.Keys[k] = S.Keys[action] end end
					S.Keys[action] = n
				end
				State.Save(); show("settings")
			end)
		end)
	end
	bigButton("Сбросить клавиши", function()
		for k, v in pairs(Config.DefaultKeys) do S.Keys[k] = v end
		State.Save(); show("settings")
	end, PANEL)

	header("ПРИЦЕЛ И КАМЕРА")
	slider("Угол обзора (FOV)", 60, 110, S.FOV, function(v) S.FOV = v end)
	slider("Размер прицела", 4, 30, S.CrosshairSize, function(v) S.CrosshairSize = v end)
	local colors = {{"Зелёный", {80, 255, 80}}, {"Красный", {255, 70, 70}}, {"Белый", {255, 255, 255}}, {"Голубой", {80, 220, 255}}, {"Жёлтый", {255, 230, 80}}}
	local row = new("Frame", {Size = UDim2.new(1, 0, 0, 38), BackgroundTransparency = 1, LayoutOrder = nextOrder()}, content)
	new("UIListLayout", {FillDirection = Enum.FillDirection.Horizontal, Padding = UDim.new(0, 6)}, row)
	for _, c in ipairs(colors) do
		button({Size = UDim2.fromOffset(96, 34), Text = c[1], TextSize = 14, BackgroundColor3 = Color3.fromRGB(c[2][1], c[2][2], c[2][3]), TextColor3 = Color3.new()}, row, function()
			S.CrosshairColor = c[2]; State.Save()
		end)
	end
	toggle("Вид от первого лица", S.FirstPerson, function(v) S.FirstPerson = v end)
	toggle("Хитмаркер", S.Hitmarker, function(v) S.Hitmarker = v end)

	header("МОБИЛЬНОЕ УПРАВЛЕНИЕ")
	slider("Размер кнопок", 0.6, 1.6, S.MobileScale, function(v) S.MobileScale = v end)
	slider("Прозрачность кнопок", 0.2, 1, S.MobileOpacity, function(v) S.MobileOpacity = v end)
	bigButton("Расставить кнопки вручную (перетаскивание)", function()
		State.Editing = true; setOpen(false)
	end, PANEL)
	bigButton("Сбросить расположение кнопок", function()
		S.MobilePos = {}; State.Save()
	end, PANEL)
end

------------------------------------------------------------ Навигация
local NAV = {
	{"В БОЙ", "deploy"}, {"ШТАБ", "home"}, {"РОЛИ", "roles"}, {"ОРУЖИЕ", "loadout"}, {"МАГАЗИН", "shop"},
	{"КРЕДИТЫ", "credits"}, {"★ VIP", "vip"}, {"ПОДДЕРЖАТЬ", "support"}, {"НАСТРОЙКИ", "settings"},
}
for _, n in ipairs(NAV) do
	local isDeploy = n[2] == "deploy"
	button({Size = UDim2.new(1, 0, 0, 40), Text = "  " .. n[1], TextXAlignment = Enum.TextXAlignment.Left,
		BackgroundColor3 = isDeploy and ACC or PANEL, TextColor3 = isDeploy and Color3.new() or TXT}, nav, function()
		if isDeploy then R.Deploy:FireServer(); setOpen(false) else show(n[2]) end
	end)
end

UIS.InputBegan:Connect(function(i, gp)
	if gp or State.Rebinding or State.Editing then return end
	if State.Matches(i, "Menu") then setOpen(not State.MenuOpen) end
end)

local lc = plr:WaitForChild("leaderstats"):WaitForChild("Credits")
lc.Changed:Connect(function() task.defer(function() State.Refresh(); refreshCredits() end) end)

repeat task.wait(.2) until State.Data
setOpen(true)
refreshCredits()
```

---

## ЧАСТЬ 8. Как всё это работает и как менять

**Таблица лидеров.** Встроенная таблица Roblox (Tab). Колонки: Kills, Deaths, Credits, игроки сгруппированы по командам «Альфа» / «Браво». Названия команд и цвета меняются в `Config.Teams`.

**Две команды.** Игроки распределяются автоматически (в команду, где меньше людей). До `Config.ScoreToWin` убийств идёт раунд, затем победа, пауза 8 сек, сброс счёта и респаун.

**Килфид.** Справа вверху: кто, чем (`[оружие]`), кого; ⌖ — хэдшот. Ваши убийства подсвечены оранжевым.

**«Откуда стрелял враг».** Красная стрелка вокруг прицела указывает направление на стрелявшего. Она вращается вместе с камерой. После смерти пишется, кто и из чего вас убил.

**Роли.** Штурмовик (граната), Медик (аптечка), Снайпер (дым), Дронщик (FPV). Роль выбирается в меню и применяется со следующего возрождения. Добавить роль: новая запись в `Config.Roles` и имя в `Config.RoleOrder`.

**FPV-дрон.** Клавиша 3 запускает дрон (роль Дронщик). Вы летите камерой дрона: WASD, пробел вверх, C вниз. Клавиша 3 ещё раз — подрыв. Касание чего угодно — взрыв. Максимум 25 сек.

**Патроны.** Подойдите к ящику (или к коробке, выпавшей с убитого) и удерживайте **E**. Ящики на карте перезаряжаются каждые 20 сек.

**Костюмы.** Подойдите к цветному ящику «Костюм: ...» и удерживайте **E**. Костюм сохраняется до конца сессии. Над шлемом всегда полоса цвета вашей команды, чтобы отличать своих.

**Еженедельные акции.** В `Config.WeeklyDeals` задано 4 акции, они ротируются сами по неделям (скидки, множитель кредитов, ускоренный откат дрона). Добавьте свои по образцу.

**VIP-пропуск.** x2 кредитов, скидка 20%, золотая винтовка «Фантом-VIP», метка [VIP].

**Донат валюты и «Поддержать меня».** Покупки за Robux через Developer Products. «Поддержать» даёт бонусные кредиты и атрибут `Supporter` игроку.

**Настройки.** Всё сохраняется в DataStore: переназначение клавиш (включая ЛКМ, C, 1, 2, 3, Z), FOV, прицел (цвет/размер), от первого лица, хитмаркер, размер и прозрачность мобильных кнопок, перетаскивание кнопок пальцем.

### Как добавить своё оружие
В `Config.Weapons` скопируйте любую запись, поменяйте ключ-название и цифры (`Damage`, `RPM`, `Mag`, `Price`...). `Slot = 1` основное, `Slot = 2` запасное. `Price = 0` — доступно сразу. Новая запись автоматически появится в магазине и экипировке.

### Свои текстуры, модели и звуки
- В `MapBuilder` меняйте `Material` и `Color3` (например, `M.Brick`, `M.Concrete`, `M.CorrodedMetal`) и числа в списке `buildings`.
- Свои модели оружия: можно заменить функцию `buildGun` загрузкой модели из `ServerStorage`.
- Звуки: в `Config.Sounds` вставьте ID вида `rbxassetid://123456`. Ассеты берите только свои или из официального Toolbox, не копируйте чужие игровые файлы.

### Известные ограничения (честно)
- Код не запускался в вашей среде, поэтому при первом тесте возможны мелкие правки. Если в Output (View → Output) появится красная ошибка, пришлите мне текст ошибки, и я исправлю.
- У оружия нет анимации удержания: модель висит в руке «от бедра». Анимации делаются отдельно в Animation Editor.
- Присед сейчас снижает камеру и скорость (визуально для других игроков персонаж не приседает без анимации).
- Пока меню открыто, персонаж не на паузе: закрывайте его перед боем.
- Клавиша подбора **E** задана ProximityPrompt и в настройках не переназначается.
- Для публикации: **File → Publish to Roblox**, затем в Creator Dashboard привяжите Game Pass и Developer Products, вставьте ID в `Config` и заново опубликуйте.
