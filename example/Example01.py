# -*- coding: utf-8 -*-
from Components import Config
from Components import SquareWaveOscillator
from Components import Amplifeir
from Components import Clock
from Components import Renderer
from Components import WaveFileSink


def main():
    osc = SquareWaveOscillator(frequency=1000.0)
    amp = Amplifeir(source=osc, gain=Config.MaxGain, attenuate=0.55555)
    sink = WaveFileSink(output_file_name="output.wav")

    clock = Clock(end=Config.SampleRate)

    renderer = Renderer(clock=clock, source=amp, sink=sink)
    renderer.do_rendering()


if __name__ == "__main__":
    main()
