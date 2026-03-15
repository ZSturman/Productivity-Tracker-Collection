//
//  TriggerRowView.swift
//  BeingAnalytics
//
//  Created by Zachary Sturman on 9/1/23.
//

import SwiftUI

struct TriggerRowView: View {
    var trigger: TempTrigger
    @Binding var showAddInputSheet: Bool
    @ObservedObject var vm: CreateActionStateVM
    @State private var inputsChanged: Bool = false
    
    var body: some View {
        Section() {
            List {
                ForEach(trigger.inputs.sorted(by: { $0.order < $1.order }), id: \.id) { input in
                    if let triggerIndex = vm.newActionState.triggers.firstIndex(where: { $0.id == trigger.id }),
                       let inputBinding = $vm.newActionState.triggers[triggerIndex].inputs.first(where: { $0.id == input.id }) {
                        InputRowView(trigger: trigger, input: inputBinding, vm: vm)
                    }

                }

                .onDelete(perform: deleteInput)
                .onMove(perform: moveInput)
                
                Button("Add Input") {
                    vm.selectedTrigger = trigger
                    showAddInputSheet.toggle()
                }
            }
        }
    }
    
    func deleteInput(at offsets: IndexSet) {
        withAnimation {
            if let offset = offsets.first {
                let inputIDToDelete = trigger.inputs.sorted(by: { $0.order < $1.order })[offset].id
                vm.deleteInput(from: trigger, inputID: inputIDToDelete)
                inputsChanged.toggle()
            }
        }
    }


    
    func moveInput(from source: IndexSet, to destination: Int) {
        withAnimation {
            vm.moveInput(in: trigger, from: source, to: destination)
            inputsChanged.toggle()
        }
    }
}
