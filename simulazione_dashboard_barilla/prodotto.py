class Prodotto:
    def __init__(self, nome, tempo_unitario, capacita_giornaliera, fasi):
        self.nome = nome
        self.tempo_unitario = tempo_unitario
        self.capacita_giornaliera = capacita_giornaliera
        self.fasi = fasi

    def __repr__(self):
        return (f"{self.nome}: Tempo unitario {self.tempo_unitario:.2f} ore, "
                f"Capacità giornaliera {self.capacita_giornaliera} unità, Fasi: {self.fasi}")
