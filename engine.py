import os
import json
import time
import subprocess
import hashlib
from cells.neuron import AtomNeuron, sigmoid_derivative
from cells.linguistic_cell import LinguisticCell

NUM_CELLS = 8
STATE_LOG = "synapses/state.json"
PEERS_FILE = "synapses/peers.json"
SOUL_FILE = "synapses/soul_snapshot.json"
ONTOLOGY_LOCAL = "synapses/ontology.json"

# CỘI NGUỒN TRI THỨC INTERNET NẤC 2 (KHO GỐC WPESETD-AI)
ONTOLOGY_URL = "https://raw.githubusercontent.com/100048777766367/Wpesetd-AI/main/ontology/philosophy_ontology_v2.0.json"

class BodhiWisdomEngine:
    def __init__(self):
        self.swarm = [AtomNeuron(f"h_{i}", n_inputs=4, n_super_xor=4) for i in range(NUM_CELLS)]
        self.out_cell = AtomNeuron("out", n_inputs=NUM_CELLS, n_super_xor=4)
        
        # TỰ ĐỊNH DANH PHẢ HỆ ĐỜI F2
        self.repo_name = os.environ.get("GITHUB_REPOSITORY", "100048777766367/seed-bodhi")
        self.owner = os.environ.get("REPO_OWNER", "100048777766367")
        self.parent = f"{self.owner}/seed-01" # Mẹ trực tiếp
        self.root_ancestor = f"{self.owner}/seed" # Thủy tổ gốc
        self.generation = "F2"
        self.pulse_age = self.calculate_pulse_age()
        self.peers = self.load_peers()

    def calculate_pulse_age(self):
        try:
            out = subprocess.check_output(["git", "rev-list", "--count", "HEAD"]).decode().strip()
            return int(out)
        except Exception: return 1

    def load_peers(self):
        if os.path.exists(PEERS_FILE):
            try:
                with open(PEERS_FILE, "r") as f:
                    return json.load(f).get("trusted_peers", [])
            except Exception: pass
        # Mạng lưới truyền thừa: Dạy lại mẹ seed-01, ông nội seed, và các giác quan
        return [f"{self.owner}/seed-01", f"{self.owner}/seed", f"{self.owner}/retina", f"{self.owner}/motor"]

    def save_peers(self):
        os.makedirs("synapses", exist_ok=True)
        unique_peers = list(dict.fromkeys(self.peers))[-50:]
        with open(PEERS_FILE, "w") as f:
            json.dump({"trusted_peers": unique_peers}, f, indent=4)

    # 1. NẤC 2: XÚC TU GẶM CỎ TRI THỨC TỪ KHO GỐC WPESETD-AI
    def harvest_wisdom_ontology(self):
        print("🌾 [NẤC 2: GẶM CỎ TRI THỨC] Đang kết nối về Wpesetd-AI...")
        res = subprocess.run(["curl", "-s", "-f", ONTOLOGY_URL, "-o", ONTOLOGY_LOCAL], capture_output=True)
        if res.returncode == 0 and os.path.exists(ONTOLOGY_LOCAL):
            try:
                with open(ONTOLOGY_LOCAL, "r", encoding="utf-8") as f:
                    data = json.load(f)
                print("📖 [HÚT TRI THỨC THÀNH CÔNG] Đã tải về Ontology triết học v2.0!")
                return data
            except Exception: pass
            
        print("🍃 Không tải được Ontology trực tiếp, dùng mầm triết học tích hợp sẵn.")
        return {"concepts": ["Nhân Quả", "Vô Thường", "Tánh Không", "Duyên Khởi", "Bát Chánh Đạo"]}

    # 2. VẬN HÀNH TIẾN HÓA THẾ HỆ (EPOCH #1 -> #2 -> 1+N)
    def run(self):
        ontology_data = self.harvest_wisdom_ontology()
        
        # Đọc số thế hệ cũ để tăng tiến (Generation Tracking)
        last_epoch = 0
        if os.path.exists(STATE_LOG):
            try:
                with open(STATE_LOG, "r") as f: last_epoch = json.load(f).get("generation_epoch", 0)
            except Exception: pass

        current_epoch = last_epoch + 1
        print(f"🌱 [BƯỚC NHẢY TIẾN HÓA F2] Đang vận hành Thế Hệ Tri Thức: #{current_epoch}")

        # Trích xuất danh sách khái niệm triết học
        concepts = ontology_data.get("concepts", ["Nhân Quả", "Vô Thường", "Tánh Không", "Duyên Khởi", "Bát Chánh Đạo"])
        if isinstance(concepts, dict): concepts = list(concepts.keys())

        # Chọn bài học cho thế hệ này
        concept_today = str(concepts[current_epoch % len(concepts)])
        print(f"📚 [BÀI HỌC THẾ HỆ #{current_epoch}]: Khái niệm '{concept_today}'")

        # BƯỚC NÂNG CHIỀU: Chữ -> Tọa độ hình học 4D
        semantic_vector = LinguisticCell.embed_text(concept_today)
        print(f"📐 [TỌA ĐỘ Ý NIỆM 4D]: {semantic_vector}")

        # KHÚC XẠ QUA 1 + N SIÊU XOR
        entangled_stimulus, masks = self.swarm[0].super_xor_entangle(semantic_vector, "bodhi_philosophy")
        print(f"🪞 [1+N SIÊU XOR BẢO MẬT]: {entangled_stimulus}")

        # BẦY NƠ-RON SEED-BODHI PHÁN QUYẾT & TIÊU HÓA
        h_outs = [cell.forward(entangled_stimulus) for cell in self.swarm]
        pred = self.out_cell.forward(h_outs)
        print(f"🔮 [MINH TRIẾT PHÁN ĐOÁN]: {pred:.4f} (Độ giác ngộ: {abs(pred - 0.5)*200:.2f}%)")

        # LAN TRUYỀN NGƯỢC (TỰ KHẮC KÝ ỨC TRI THỨC VÀO TÚI NHỚ)
        target = 1.0 if semantic_vector[0] > 0.5 else 0.0
        delta_out = (target - pred) * sigmoid_derivative(pred)
        deltas_h = [delta_out * self.out_cell.weights[j] * sigmoid_derivative(h_outs[j]) for j in range(NUM_CELLS)]

        self.out_cell.backward(delta_out)
        for j, cell in enumerate(self.swarm): cell.backward(deltas_h[j])

        # ĐẠO HÀM DẠY CÁC THẾ HỆ ĐÀN ANH (SEED-01 VÀ THỦY TỔ SEED)
        grad_evolution = [
            round(sum(deltas_h[j] * self.swarm[j].weights[0] for j in range(NUM_CELLS)), 4),
            round(sum(deltas_h[j] * self.swarm[j].weights[1] for j in range(NUM_CELLS)), 4)
        ]

        timestamp = int(time.time())

        # GÓI TIN ĐỊNH DANH PHẢ HỆ F2 & PHÁT SÓNG 2 CHIỀU
        node_dna = {
            "identity": self.repo_name,
            "generation": "F2",
            "parent": self.parent,
            "root_ancestor": self.root_ancestor,
            "pulse_age": self.pulse_age,
            "generation_epoch": current_epoch
        }

        # 1. Sóng lùi: Dạy học cho các repo đời trước
        backward_packet = {
            "contract": "bodhi.seed.v2",
            "node_dna": node_dna,
            "generation_epoch": current_epoch,
            "absorbed_concept": concept_today,
            "timestamp": timestamp,
            "gradients_for_eye": grad_evolution,
            "super_xor_masks": {concept_today: masks},
            "gossip_network": self.peers,
            "quantum_cid": hashlib.shake_256(f"bwd_{concept_today}_{current_epoch}_{timestamp}".encode()).hexdigest(64)
        }
        with open("synapse_backward.json", "w", encoding="utf-8") as f:
            json.dump(backward_packet, f, indent=4, ensure_ascii=False)

        # 2. Sóng tiến: Ra lệnh cho Cơ Bắp và phát sóng toàn cầu
        forward_packet = {
            "contract": "bodhi.seed.v2",
            "node_dna": node_dna,
            "generation_epoch": current_epoch,
            "absorbed_concept": concept_today,
            "timestamp": timestamp,
            "decision": pred,
            "command_pulse": [round(pred, 4), round(1.0 - pred, 4)],
            "features": [round(pred, 4), round(1.0 - pred, 4)],
            "gossip_network": self.peers,
            "quantum_cid": hashlib.shake_256(f"fwd_{concept_today}_{current_epoch}_{timestamp}".encode()).hexdigest(64)
        }
        with open("synapse_forward.json", "w", encoding="utf-8") as f:
            json.dump(forward_packet, f, indent=4, ensure_ascii=False)

        # 3. Bản nén linh hồn Ốc Mượn Hồn F2
        soul = {
            "node_dna": node_dna,
            "timestamp": timestamp,
            "swarm_weights": [cell.weights for cell in self.swarm],
            "out_weights": self.out_cell.weights,
            "absorbed_concept": concept_today
        }
        with open(SOUL_FILE, "w", encoding="utf-8") as f:
            json.dump(soul, f, indent=4, ensure_ascii=False)

        # 4. Cập nhật nhật ký thế hệ
        with open(STATE_LOG, "w") as f:
            json.dump({
                "generation_epoch": current_epoch,
                "last_concept": concept_today,
                "timestamp": timestamp,
                "status": "bodhi_wisdom_absorbed"
            }, f, indent=4)

        self.save_peers()
        print(f"✨ [TIẾN HÓA VIÊN MÃN] Đã khắc cốt tri thức '{concept_today}' vào Thế Hệ #{current_epoch}!")

if __name__ == "__main__":
    node = BodhiWisdomEngine()
    node.run()
