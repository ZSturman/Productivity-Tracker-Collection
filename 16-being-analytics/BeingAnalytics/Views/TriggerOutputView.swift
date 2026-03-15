//
//  TriggerOutputView().swift
//  BeingAnalytics
//
//  Created by Zachary Sturman on 9/1/23.
// 

import SwiftUI

struct TriggerOutputView: View {
    @ObservedObject var vm: CreateActionStateVM
    @State private var currentTrigger: TempTrigger
    
    init(vm: CreateActionStateVM, trigger: TempTrigger) {
        self.vm = vm
        _currentTrigger = State(initialValue: trigger)
    }
    
    var body: some View {
        VStack {
            VStack {
                Text(currentTrigger.triggerOutputDate)
            }
            .frame(maxWidth: .infinity, alignment: .leading)
            
            if currentTrigger.getLocation == true {
                VStack {
                    Text(currentTrigger.triggerOutputLocation ?? "")
                }
                .frame(maxWidth: .infinity, alignment: .leading)
            }
            
            VStack {
                Text(currentTrigger.inputs.last?.inputOutput ?? "")

            }
            .frame(maxWidth: .infinity, alignment: .trailing)
        }
        .onAppear() {
            currentTrigger = vm.updateTriggerOutputs(for: currentTrigger)
        }
    }
}
